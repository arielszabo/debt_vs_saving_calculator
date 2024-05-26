from typing import Optional


def get_calculation_text(total_portfolio_amount: float,
                         portfolio_interest_amount: float,
                         bank_yearly_interest_rate_on_a_loan: float,
                         loan_length_in_month: int,
                         loan_amount: float,
                         expected_yearly_return_rate: float,
                         portfolio_after_expense_without_loan: float,
                         monthly_contribution_or_loan_payback: float,
                         without_loan_portfolio_end_size: float,
                         total_loan_payback_amount: float,
                         with_loan_portfolio_end_size: float,
                         randomization_monthly_return_factor: Optional[float],
                         randomized_drop_in_portfolio: Optional[float],
                         is_loan_worth_it: bool
                         ) -> str:
    return f"""
For a loan of ${__format_number(loan_amount)} for {loan_length_in_month} months
with portfolio of size ${__format_number(total_portfolio_amount)} (${__format_number(portfolio_interest_amount)} of them are gains)
and a {100 * bank_yearly_interest_rate_on_a_loan:.2f}% yearly interest on the loan,
while expecting {100 * expected_yearly_return_rate:.2f}% yearly return from investments.
{f'* with a +-{100 * randomization_monthly_return_factor}% max of random change in return every month' if randomization_monthly_return_factor is not None else ''}
{f'** with a random drop of {100 * randomized_drop_in_portfolio}% in one month.' if randomized_drop_in_portfolio is not None else ''} 

Option 1 - Pull from savings:
The amount you will need to pull from your investments is ${__format_number(total_portfolio_amount - portfolio_after_expense_without_loan)}.
After paying for the expense you will invest ${__format_number(monthly_contribution_or_loan_payback)} every month
and your final portfolio size after {loan_length_in_month} month would be:
${__format_number(without_loan_portfolio_end_size)}

Option 2 - Get a loan:
The amount you will be paying on the loan will be ${__format_number(total_loan_payback_amount)}
Your monthly paybacks will be ${__format_number(monthly_contribution_or_loan_payback)}
and your final portfolio size after {loan_length_in_month} month would be:
${__format_number(with_loan_portfolio_end_size)}

Is a loan worth is: {'Yes!' if is_loan_worth_it else 'No!'}
"""


def __format_number(large_number: float) -> str:
    absolute_large_number = abs(large_number)

    unit_scale_to_suffix = {
        1_000_000_000_000: "T",
        1_000_000_000: "B",
        1_000_000: "M",
        1_000: "K"
    }
    for unit_scale, suffix in unit_scale_to_suffix.items():
        if absolute_large_number >= unit_scale:
            if large_number % unit_scale == 0:
                return f"{large_number // unit_scale}{suffix}"
            else:
                return f"{round(large_number / unit_scale, 2)}{suffix}"

    return str(large_number)
