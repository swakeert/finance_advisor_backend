from rest_framework import routers

from finance_advisor.cash_flows.views import AdviseeExpenseViewset, AdviseeIncomeViewset

advisee_cash_flow_router = routers.DefaultRouter()
advisee_cash_flow_router.register("incomes", AdviseeIncomeViewset, "advisee-incomes")
advisee_cash_flow_router.register("expenses", AdviseeExpenseViewset, "advisee-expenses")
