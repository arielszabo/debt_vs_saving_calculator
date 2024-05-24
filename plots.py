import statistics

import pandas as pd
import matplotlib

from main import calculate_if_loan_is_worth

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns

TOTAL_PORTFOLIO_AMOUNT = 500_000
PORTFOLIO_INTEREST_AMOUNT = 70_000
LOAN_AMOUNT = 200_000
LOAN_LENGTH_IN_MONTH = 12

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
