from main import __get_monthly_return_rates, __get_portfolio_size_after


def test__get_portfolio_size_after():
    monthly_return_rates = __get_monthly_return_rates(expected_yearly_return_rate=0.05,
                                                      month_amount=12,
                                                      randomized_drop_in_portfolio=None,
                                                      randomization_monthly_return_factor=None)
    assert round(__get_portfolio_size_after(start_portfolio=100,
                                            monthly_contribution=0,
                                            monthly_return_rates=monthly_return_rates), 4) == 105
