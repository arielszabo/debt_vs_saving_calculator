import math


def calculate_if_loan_is_worth(
        total_portfolio_amount: float,
        portfolio_interest_amount: float,
        bank_yearly_interest_on_a_loan: float,
        loan_length_in_month: int,
        loan_amount: float,
        expected_yearly_return_rate: float,    # TODO: calculate based on past investments ?
        capital_gains_tax_percentage: float = 25,
        # randomization_factor_for_monthly_return: float = 0,  # TODO: explain
) -> bool:
    """
    Assumptions:
    1) Your portfolio is profitable, meaning you don't have loses. TODO: add an option to calculate losses as well where you don't pay taxes
    2) You don't add any more money to your portfolio until you pay back the loan.

    :param total_portfolio_amount:
    :param portfolio_interest_amount:
    :param bank_yearly_interest_on_a_loan:
    :param loan_length_in_month:
    :param loan_amount:
    :param expected_yearly_return_rate:
    :param capital_gains_tax_percentage:
    :return:
    """
    ...
    need_to_get_from_portfolio_gains = (100 * loan_amount) / (100 - capital_gains_tax_percentage)
    print(f"{need_to_get_from_portfolio_gains = :,.2f}")
    if need_to_get_from_portfolio_gains <= portfolio_interest_amount:
        portfolio_amount_after_expense_without_loan = total_portfolio_amount - need_to_get_from_portfolio_gains
    else:
        raise NotImplementedError()

    without_loan_portfolio_end_size = __get_without_loan_portfolio_end_size(portfolio_amount_after_expense_without_loan,
                                                                            loan_amount,
                                                                            loan_length_in_month,
                                                                            bank_yearly_interest_on_a_loan,
                                                                            expected_yearly_return_rate)

    with_loan_portfolio_end_size = total_portfolio_amount

    print(f"{with_loan_portfolio_end_size    = :,.2f}")
    print(f"{without_loan_portfolio_end_size = :,.2f}")
    return with_loan_portfolio_end_size > without_loan_portfolio_end_size


def __get_without_loan_portfolio_end_size(
        portfolio_amount_after_expense_without_loan: float,
        loan_amount: float,
        loan_length_in_month: int,
        bank_yearly_interest_on_a_loan: float,
        expected_yearly_return_rate: float,
) -> float:
    total_loan_payback_amount = loan_amount * (loan_length_in_month / 12) * (1 + (bank_yearly_interest_on_a_loan / 100))
    print(f"{total_loan_payback_amount = :,.2f}")

    monthly_investment_contribution_or_loan_payback = loan_amount / loan_length_in_month

    expected_monthly_return_rate = math.pow(1 + expected_yearly_return_rate / 100, 1 / 12)
    print(f"{expected_monthly_return_rate = :,.4f}")

    without_loan_portfolio_end_size = portfolio_amount_after_expense_without_loan
    for _ in range(loan_length_in_month):
        without_loan_portfolio_end_size = (without_loan_portfolio_end_size + monthly_investment_contribution_or_loan_payback) * expected_monthly_return_rate
        print(f"after {_:<2} month: {without_loan_portfolio_end_size = :,.2f}")
    return without_loan_portfolio_end_size


if __name__ == '__main__':
    print(calculate_if_loan_is_worth(total_portfolio_amount=500_000,
                                     portfolio_interest_amount=200_000,
                                     bank_yearly_interest_on_a_loan=6,
                                     loan_length_in_month=12,
                                     loan_amount=100_000,
                                     expected_yearly_return_rate=5,
                                     ))
