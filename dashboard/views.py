from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from expense_tracker.utils import UserQuerySetMixin
from django.db.models import Sum
from expenses.models import Expense
from income.models import Income

class DashboardSummaryAPIView(APIView):
    """
    API Endpoint: /api/dashboard/summary/
    Method: GET
    
    Goal: Return total Income, Expense, Net Profit, and Transaction Count.
    Params: ?month=YYYY-MM (Optional)
    """
    # Force authentication: Only logged-in users can access this endpoint.
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Calculates financial summary for the authenticated user.
        Optional: filters by 'month' query param (YYYY-MM).
        """
        # 1. Identity: Get the currently logged-in user from the request token.
        user = request.user
        
        # 2. Input: Check if user provided a specific month (e.g., ?month=2026-01).
        month = request.query_params.get('month') 

        # 3. Scope: Start with ALL records that belong to THIS user.
        # This ensures data isolation (User A cannot see User B's data).
        expenses = Expense.objects.filter(owner=user)
        incomes = Income.objects.filter(owner=user)

        # 4. Filtering: If a month was provided, narrow down the querysets.
        # 'entry_date__startswith' is a Django shortcut for filtering text-based dates or date objects.
        if month:
            expenses = expenses.filter(entry_date__startswith=month)
            incomes = incomes.filter(entry_date__startswith=month)

        # 5. Aggregation: Calculate totals using Database Sum.
        # aggregate() runs a SQL SUM query. 
        # - SELECT SUM("expenses_expense"."amount") AS "amount__sum" FROM "expenses_expense" WHERE ----
        # ['amount__sum'] is the default key Django uses for the result.
        # 'or 0' ensures we return 0 instead of None if there are no records.
        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # 6. Calculation: Compute logic in Python
        net_profit = total_income - total_expense
        api_transaction_count = expenses.count() + incomes.count()

        # 7. Response: Return a simple JSON dictionary.
        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "net_profit": net_profit,
            "transaction_count": api_transaction_count,
            "filter_month": month or "All Time"
        }, status=status.HTTP_200_OK)


class DashboardStatsAPIView(APIView):
    """
    API Endpoint: /api/dashboard/stats/
    Method: GET
    
    Goal: Return aggregated data by category (for charts).
    Params: ?month=YYYY-MM (Optional)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Groups expenses and income by 'category' and sums the amounts.
        Useful for Pie Charts or Bar Charts.
        """
        user = request.user
        month = request.query_params.get('month')

        # --- Expense Logic ---
        # 1. Filter: Get user's expenses (and optional month filter)
        expenses = Expense.objects.filter(owner=user)
        if month:
            expenses = expenses.filter(entry_date__startswith=month)

        # 2. Group By: Use 'values()' and 'annotate()'.
        # values('category__name'): corresponds to SQL 'GROUP BY category_name'
        # annotate(total=Sum('amount')): corresponds to SQL 'SUM(amount) as total'
        # order_by('-total'): Sorts descending so highest spending is first.
        expense_by_category = expenses.values('category__name').annotate(total=Sum('amount')).order_by('-total')
        
        # --- Income Logic ---
        # Same logic applied to Income
        incomes = Income.objects.filter(owner=user)
        if month:
            incomes = incomes.filter(entry_date__startswith=month)

        income_by_category = incomes.values('category__name').annotate(total=Sum('amount')).order_by('-total')

        # 3. Response: Return two lists of category data
        return Response({
            "expense_by_category": expense_by_category,
            "income_by_category": income_by_category
        }, status=status.HTTP_200_OK)
