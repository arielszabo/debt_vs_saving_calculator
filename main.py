import math
import random
import statistics

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns


def calculate_if_loan_is_worth(
        total_portfolio_amount: float,
        portfolio_interest_amount: float,
        bank_yearly_interest_rate_on_a_loan: float,
        loan_length_in_month: int,
        loan_amount: float,
        expected_yearly_return_rate: float,    # TODO: calculate based on past investments ?
        capital_gains_tax_rate: float = 0.25,
        randomization_monthly_return_factor: float = 0,  # TODO: explain
        verbose: bool = True,
) -> bool:
    """
    Assumptions:
    1) Your portfolio is profitable, meaning you don't have loses. TODO: add an option to calculate losses as well where you don't pay taxes
    2) You don't add any more money to your portfolio until you pay back the loan.

    :param total_portfolio_amount:
    :param portfolio_interest_amount:
    :param bank_yearly_interest_rate_on_a_loan:
    :param loan_length_in_month:
    :param loan_amount:
    :param expected_yearly_return_rate:
    :param capital_gains_tax_rate: 25% -> 0.25
    :param randomization_monthly_return_factor:
    :param verbose:
    :return:
    """
    need_to_get_from_portfolio_gains = loan_amount / (1 - capital_gains_tax_rate)
    # print(f"{need_to_get_from_portfolio_gains = :,.2f}")
    if need_to_get_from_portfolio_gains <= portfolio_interest_amount:
        portfolio_after_expense_without_loan = total_portfolio_amount - need_to_get_from_portfolio_gains
    else:
        amount_from_portfolio_gains = portfolio_interest_amount * (1 - capital_gains_tax_rate)
        remaining_loan_amount = loan_amount - amount_from_portfolio_gains
        portfolio_without_gains = total_portfolio_amount - portfolio_interest_amount
        portfolio_after_expense_without_loan = portfolio_without_gains - remaining_loan_amount

    # print(f"{portfolio_after_expense_without_loan = :,.2f}")

    loan_interest_rate = math.pow(1 + bank_yearly_interest_rate_on_a_loan, loan_length_in_month / 12)
    total_loan_payback_amount = loan_amount * loan_interest_rate
    # print(f"{total_loan_payback_amount = :,.2f}")

    monthly_contribution_or_loan_payback = total_loan_payback_amount / loan_length_in_month
    # print(f"{monthly_contribution_or_loan_payback = :,.2f}")

    without_loan_portfolio_end_size = __get_portfolio_size_after(start_portfolio=portfolio_after_expense_without_loan,
                                                                 monthly_contribution=monthly_contribution_or_loan_payback,
                                                                 expected_yearly_return_rate=expected_yearly_return_rate,
                                                                 month_amount=loan_length_in_month,
                                                                 randomization_monthly_return_factor=randomization_monthly_return_factor)

    with_loan_portfolio_end_size = __get_portfolio_size_after(start_portfolio=total_portfolio_amount,
                                                              monthly_contribution=0,
                                                              expected_yearly_return_rate=expected_yearly_return_rate,
                                                              month_amount=loan_length_in_month,
                                                              randomization_monthly_return_factor=randomization_monthly_return_factor)

    is_loan_worth_it = with_loan_portfolio_end_size > without_loan_portfolio_end_size  # TODO: add a risk factor
    if verbose:
        print(f"""
        For a loan of {__format_number(loan_amount)}$ for {loan_length_in_month} months
        with portfolio of size {__format_number(total_portfolio_amount)}$ ({__format_number(portfolio_interest_amount)}$ of them are gains)
        and a {100 * bank_yearly_interest_rate_on_a_loan:.2f}% yearly interest on the loan,
        while expecting {100 * expected_yearly_return_rate:.2f}% yearly return from investments (+-{100 * randomization_monthly_return_factor}% max of random change every month) 
        
        Option 1 - Pull from savings:
        The amount you will need to pull from your investments is {__format_number(total_portfolio_amount - portfolio_after_expense_without_loan)}$.
        After paying for the expense you will invest {__format_number(monthly_contribution_or_loan_payback)}$ every month
        and your final portfolio size after {loan_length_in_month} month would be:
        {__format_number(without_loan_portfolio_end_size)}$
        
        Option 2 - Get a loan:
        The amount you will be paying on the loan will be {__format_number(total_loan_payback_amount)}$
        Your monthly paybacks will be {__format_number(monthly_contribution_or_loan_payback)}$
        and your final portfolio size after {loan_length_in_month} month would be:
        {__format_number(with_loan_portfolio_end_size)}$
         
        Is a loan worth is: {'Yes!' if is_loan_worth_it else 'No!'}
        """)
    return is_loan_worth_it


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
                return f"~{round(large_number / unit_scale, 2)}{suffix}"

    return str(large_number)


def __get_portfolio_size_after(start_portfolio: float,
                               monthly_contribution: float,
                               expected_yearly_return_rate: float,
                               month_amount: int,
                               randomization_monthly_return_factor: float,
                               ) -> float:
    expected_monthly_return_rate = math.pow(1 + expected_yearly_return_rate, 1 / 12)
    # print(f"{expected_monthly_return_rate = :,.4f}")

    portfolio_size = start_portfolio
    for _ in range(month_amount):
        randomized_rate = random.random() * randomization_monthly_return_factor
        if random.random() > 0.5:
            randomized_rate = -randomized_rate
        # print(f"after {_:<2} month: {100 * randomized_rate = :,.2f}%")
        month_return_rate = expected_monthly_return_rate + randomized_rate
        portfolio_size = (portfolio_size + monthly_contribution) * month_return_rate

    return portfolio_size


if __name__ == '__main__':
    TOTAL_PORTFOLIO_AMOUNT = 500_000
    PORTFOLIO_INTEREST_AMOUNT = 70_000
    LOAN_AMOUNT = 200_000
    LOAN_LENGTH_IN_MONTH = 12
    calculate_if_loan_is_worth(total_portfolio_amount=TOTAL_PORTFOLIO_AMOUNT,
                               portfolio_interest_amount=PORTFOLIO_INTEREST_AMOUNT,
                               bank_yearly_interest_rate_on_a_loan=0.08,
                               loan_length_in_month=LOAN_LENGTH_IN_MONTH,
                               loan_amount=LOAN_AMOUNT,
                               expected_yearly_return_rate=0.07,
                               randomization_monthly_return_factor=0,
                               )

    rate_values = [(i / 100) for i in range(20)]
    data = []
    for bank_yearly_interest_rate_on_a_loan in rate_values:
        for expected_yearly_return_rate in rate_values:
            results = []
            for _ in range(1_000):
                result = calculate_if_loan_is_worth(total_portfolio_amount=TOTAL_PORTFOLIO_AMOUNT,
                                                    portfolio_interest_amount=PORTFOLIO_INTEREST_AMOUNT,
                                                    bank_yearly_interest_rate_on_a_loan=bank_yearly_interest_rate_on_a_loan,
                                                    loan_length_in_month=LOAN_LENGTH_IN_MONTH,
                                                    loan_amount=LOAN_AMOUNT,
                                                    expected_yearly_return_rate=expected_yearly_return_rate,
                                                    randomization_monthly_return_factor=0.01,
                                                    verbose=False)
                results.append(result)
            final_result = statistics.mode(results)
            data.append([100 * bank_yearly_interest_rate_on_a_loan, 100 * expected_yearly_return_rate, final_result])

    # print(data)

    df = pd.DataFrame(data, columns=["bank_yearly_interest_rate_on_a_loan", "expected_yearly_return_rate", "result"])
    sns.scatterplot(data=df, x="bank_yearly_interest_rate_on_a_loan", y="expected_yearly_return_rate", hue="result")
    plt.show()
