import math
import random
from typing import Optional


def calculate_if_loan_is_worth(
        total_portfolio_amount: float,
        portfolio_interest_amount: float,
        bank_yearly_interest_rate_on_a_loan: float,
        loan_length_in_month: int,
        loan_amount: float,
        expected_yearly_return_rate: float,    # TODO: calculate based on past investments ?
        randomization_monthly_return_factor: Optional[float] = None,  # TODO: explain
        randomized_drop_in_portfolio: Optional[float] = None,  # TODO: explain
        verbose: bool = True,
) -> bool:
    """
    Assumptions:
    1) Your portfolio is profitable, meaning you don't have loses. TODO: add an option to calculate losses as well where you don't pay taxes
    2) You don't add any more money to your portfolio until you pay back the loan.
    3) The loan interest rate does not grow TODO: add a parameter for this as well
    4) The investment return can be negative TODO: add a parameter for this as well, maybe calculate it based on history

    :param total_portfolio_amount:
    :param portfolio_interest_amount:
    :param bank_yearly_interest_rate_on_a_loan:
    :param loan_length_in_month:
    :param loan_amount:
    :param expected_yearly_return_rate:
    :param randomization_monthly_return_factor:
    :param randomized_drop_in_portfolio
    :param verbose:
    :return:
    """
    loan_interest_rate = math.pow(1 + bank_yearly_interest_rate_on_a_loan, loan_length_in_month / 12)
    total_loan_payback_amount = loan_amount * loan_interest_rate

    monthly_contribution_or_loan_payback = total_loan_payback_amount / loan_length_in_month

    portfolio_after_expense_without_loan = __get_portfolio_after_expense_without_loan(total_portfolio_amount=total_portfolio_amount,
                                                                                      portfolio_interest_amount=portfolio_interest_amount,
                                                                                      loan_amount=loan_amount)

    monthly_return_rates = __get_monthly_return_rates(expected_yearly_return_rate=expected_yearly_return_rate,
                                                      month_amount=loan_length_in_month,
                                                      randomization_monthly_return_factor=randomization_monthly_return_factor,
                                                      randomized_drop_in_portfolio=randomized_drop_in_portfolio
                                                      )  # use the same monthly return rates for the 2 scenarios
    without_loan_portfolio_end_size = __get_portfolio_size_after(start_portfolio=portfolio_after_expense_without_loan,
                                                                 monthly_contribution=monthly_contribution_or_loan_payback,
                                                                 monthly_return_rates=monthly_return_rates)

    with_loan_portfolio_end_size = __get_portfolio_size_after(start_portfolio=total_portfolio_amount,
                                                              monthly_contribution=0,
                                                              monthly_return_rates=monthly_return_rates)

    is_loan_worth_it = with_loan_portfolio_end_size > without_loan_portfolio_end_size  # TODO: add a risk factor for example a margin of $ that have to be added to the portfolioo with loan before the comparison to represent the risk of the loan
    if verbose:
        print(f"""
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
        """)
    return is_loan_worth_it


def __get_portfolio_after_expense_without_loan(
        total_portfolio_amount: float,
        portfolio_interest_amount: float,
        loan_amount: float,
        capital_gains_tax_rate: float = 0.25,
) -> float:
    need_to_get_from_portfolio_gains = loan_amount / (1 - capital_gains_tax_rate)
    if need_to_get_from_portfolio_gains <= portfolio_interest_amount:
        portfolio_after_expense_without_loan = total_portfolio_amount - need_to_get_from_portfolio_gains
    else:
        amount_from_portfolio_gains = portfolio_interest_amount * (1 - capital_gains_tax_rate)
        remaining_loan_amount = loan_amount - amount_from_portfolio_gains
        portfolio_without_gains = total_portfolio_amount - portfolio_interest_amount
        portfolio_after_expense_without_loan = portfolio_without_gains - remaining_loan_amount
    return portfolio_after_expense_without_loan


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


def __get_portfolio_size_after(start_portfolio: float,
                               monthly_contribution: float,
                               monthly_return_rates: list[float],
                               ) -> float:

    portfolio_size = start_portfolio
    for month_return_rate in monthly_return_rates:
        portfolio_size = (portfolio_size + monthly_contribution) * month_return_rate

    return portfolio_size


def __get_monthly_return_rates(
        expected_yearly_return_rate: float,
        month_amount: int,
        randomization_monthly_return_factor: Optional[float],
        randomized_drop_in_portfolio: Optional[float],
) -> list[float]:
    expected_monthly_return_rate = math.pow(1 + expected_yearly_return_rate, 1 / 12)
    monthly_return_rates = [expected_monthly_return_rate for _ in range(month_amount)]

    if randomization_monthly_return_factor is not None:
        randomization_monthly_return_rates = []
        for monthly_return_rate in monthly_return_rates:
            randomized_rate = random.uniform(-randomization_monthly_return_factor, randomization_monthly_return_factor)
            randomization_monthly_return_rates.append(monthly_return_rate + randomized_rate)
        monthly_return_rates = randomization_monthly_return_rates

    if randomized_drop_in_portfolio is not None:
        random_moth_index = random.randint(0, len(monthly_return_rates) - 1)
        monthly_return_rates[random_moth_index] = 1 + randomized_drop_in_portfolio

    return monthly_return_rates


if __name__ == '__main__':
    calculate_if_loan_is_worth(total_portfolio_amount=500_000,
                               portfolio_interest_amount=70_000,
                               bank_yearly_interest_rate_on_a_loan=0.08,
                               loan_length_in_month=12,
                               loan_amount=100_000,
                               expected_yearly_return_rate=0.07,
                               randomization_monthly_return_factor=None,
                               randomized_drop_in_portfolio=-0.3,
                               )
