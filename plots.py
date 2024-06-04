import statistics

import pandas as pd
import matplotlib
from tqdm import tqdm

from main import calculate_if_loan_is_worth

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns

TOTAL_PORTFOLIO_AMOUNT = 1_000_000
PORTFOLIO_INTEREST_AMOUNT = 100_000
LOAN_AMOUNT = 100_000
LOAN_LENGTH_IN_MONTH = 12
RANDOMIZATION_MONTHLY_RETURN_FACTOR = 0.01
RANDOMIZED_DROP_IN_PORTFOLIO = -0.3


bank_yearly_interest_rate_on_a_loan_values = [(i / 100) for i in range(20)]
expected_yearly_return_rate_values = [(i / 100) for i in range(20)] + [-(i / 100) for i in range(20)]
random_sample_size = 1_000
progress_bar = tqdm(total=random_sample_size * len(expected_yearly_return_rate_values) * len(bank_yearly_interest_rate_on_a_loan_values))

data = []
for bank_yearly_interest_rate_on_a_loan in bank_yearly_interest_rate_on_a_loan_values:
    for expected_yearly_return_rate in expected_yearly_return_rate_values:
        results = []
        for _ in range(random_sample_size):
            result = calculate_if_loan_is_worth(total_portfolio_amount=TOTAL_PORTFOLIO_AMOUNT,
                                                portfolio_interest_amount=PORTFOLIO_INTEREST_AMOUNT,
                                                bank_yearly_interest_rate_on_a_loan=bank_yearly_interest_rate_on_a_loan,
                                                loan_length_in_month=LOAN_LENGTH_IN_MONTH,
                                                loan_amount=LOAN_AMOUNT,
                                                expected_yearly_return_rate=expected_yearly_return_rate,
                                                randomization_monthly_return_factor=RANDOMIZATION_MONTHLY_RETURN_FACTOR,
                                                randomized_drop_in_portfolio=RANDOMIZED_DROP_IN_PORTFOLIO,
                                                verbose=False)
            results.append(result)
            progress_bar.update(1)
        final_result = statistics.mode(results)
        data.append([100 * bank_yearly_interest_rate_on_a_loan, 100 * expected_yearly_return_rate, final_result])

# print(data)

df = pd.DataFrame(data, columns=["bank_yearly_interest_rate_on_a_loan", "expected_yearly_return_rate", "result"])
sns.scatterplot(data=df, x="bank_yearly_interest_rate_on_a_loan", y="expected_yearly_return_rate", hue="result")
plt.show()
