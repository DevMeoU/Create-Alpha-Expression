OPERATORS = {
    "Arithmetic": [
        {
            "name": "abs(x)",
            "description": "Absolute value of x"
        },
        {
            "name": "add(x, y, filter=false)",
            "description": "x + y; add all inputs (>=2). If filter=true, NaN -> 0 before adding"
        },
        {
            "name": "densify(x)",
            "description": "Converts a grouping field of many buckets into fewer buckets (for efficiency)"
        },
        {
            "name": "divide(x, y)",
            "description": "x / y"
        },
        {
            "name": "inverse(x)",
            "description": "1 / x"
        },
        {
            "name": "log(x)",
            "description": "Natural logarithm of x"
        },
        {
            "name": "max(x, y, ...)",
            "description": "Maximum value among inputs (>=2)"
        },
        {
            "name": "min(x, y, ...)",
            "description": "Minimum value among inputs (>=2)"
        },
        {
            "name": "multiply(x, y, ..., filter=false)",
            "description": "x * y; multiply all inputs (>=2). If filter=true, NaN -> 1"
        },
        {
            "name": "power(x, y)",
            "description": "x ^ y"
        },
        {
            "name": "reverse(x)",
            "description": "-x"
        },
        {
            "name": "sign(x)",
            "description": "Sign of x; if x=NaN, return NaN"
        },
        {
            "name": "signed_power(x, y)",
            "description": "x^y, preserving the sign of x"
        },
        {
            "name": "subtract(x, y, filter=false)",
            "description": "x - y; if filter=true, NaN -> 0 before subtracting"
        }
    ],
    "Logical": [
        {
            "name": "and(input1, input2)",
            "description": "Logical AND; true if both operands are true"
        },
        {
            "name": "if_else(input1, input2, input3)",
            "description": "If input1 is true => input2 else input3"
        },
        {
            "name": "input1 < input2",
            "description": "Returns true if input1 < input2"
        },
        {
            "name": "input1 <= input2",
            "description": "Returns true if input1 <= input2"
        },
        {
            "name": "input1 == input2",
            "description": "Returns true if both inputs are the same"
        },
        {
            "name": "input1 > input2",
            "description": "Returns true if input1 > input2"
        },
        {
            "name": "input1 >= input2",
            "description": "Returns true if input1 >= input2"
        },
        {
            "name": "input1 != input2",
            "description": "Returns true if input1 != input2"
        },
        {
            "name": "is_nan(input)",
            "description": "Returns 1 if input == NaN, else 0"
        },
        {
            "name": "not(x)",
            "description": "Logical NOT; if x=1 => 0, if x=0 => 1"
        },
        {
            "name": "or(input1, input2)",
            "description": "Logical OR; true if either operand is true"
        }
    ],
    "Time Series": [
        {
            "name": "days_from_last_change(x)",
            "description": "Days since last change of x"
        },
        {
            "name": "hump(x, hump=0.01)",
            "description": "Limits magnitude/frequency of changes in x (reduce turnover)"
        },
        {
            "name": "kth_element(x, d, k)",
            "description": "Returns K-th value of x from last d days"
        },
        {
            "name": "last_diff_value(x, d)",
            "description": "Returns last x value (within d days) that differs from current x"
        },
        {
            "name": "ts_arg_max(x, d)",
            "description": "Relative index of max value in past d days (0 if max is today)"
        },
        {
            "name": "ts_arg_min(x, d)",
            "description": "Relative index of min value in past d days (0 if min is today)"
        },
        {
            "name": "ts_av_diff(x, d)",
            "description": "x - ts_mean(x,d), ignoring NaNs in mean"
        },
        {
            "name": "ts_backfill(x, lookback=d, k=1, ignore='NAN')",
            "description": "Backfill NaN/0 values by first non-NaN in last d days"
        },
        {
            "name": "ts_corr(x, y, d)",
            "description": "Correlation of x and y over past d days"
        },
        {
            "name": "ts_count_nans(x, d)",
            "description": "Number of NaN values in x for the past d days"
        },
        {
            "name": "ts_covariance(y, x, d)",
            "description": "Covariance of y and x for the past d days"
        },
        {
            "name": "ts_decay_linear(x, d, dense=false)",
            "description": "Linear decay over past d days; dense=false => treat NaN as 0"
        },
        {
            "name": "ts_delay(x, d)",
            "description": "Returns x's value d days ago"
        },
        {
            "name": "ts_delta(x, d)",
            "description": "x - ts_delay(x, d)"
        },
        {
            "name": "ts_mean(x, d)",
            "description": "Average of x over past d days"
        },
        {
            "name": "ts_product(x, d)",
            "description": "Product of x over past d days"
        },
        {
            "name": "ts_quantile(x, d, driver='gaussian')",
            "description": "Computes ts_rank, then applies inverse CDF (gaussian, cauchy, uniform)"
        },
        {
            "name": "ts_rank(x, d, constant=0)",
            "description": "Rank of x in past d days (0 if default), returns rank of current day"
        },
        {
            "name": "ts_regression(y, x, d, lag=0, rettype=0)",
            "description": "Regression of y on x over past d days, returns parameter depending on rettype"
        },
        {
            "name": "ts_scale(x, d, constant=0)",
            "description": "(x - ts_min)/(ts_max - ts_min) + constant over d days"
        },
        {
            "name": "ts_std_dev(x, d)",
            "description": "Standard deviation of x over past d days"
        },
        {
            "name": "ts_step(1), step(1)",
            "description": "Day counter"
        },
        {
            "name": "ts_sum(x, d)",
            "description": "Sum of x over past d days"
        },
        {
            "name": "ts_zscore(x, d)",
            "description": "Z-score: (x - mean)/std over d days"
        }
    ],
    "Cross Sectional": [
        {
            "name": "normalize(x, useStd=false, limit=0.0)",
            "description": "Subtract mean of x (per date). If useStd=true, also divide by std"
        },
        {
            "name": "quantile(x, driver='gaussian', sigma=1.0)",
            "description": "Rank x then apply distribution transform (gaussian/cauchy/uniform)"
        },
        {
            "name": "rank(x, rate=2)",
            "description": "Rank among instruments => [0..1]. rate=0 => precise sort"
        },
        {
            "name": "scale(x, scale=1, longscale=1, shortscale=1)",
            "description": "Scale input to booksize or separate scaling for long/short"
        },
        {
            "name": "winsorize(x, std=4)",
            "description": "Clamp x within mean ± 4*std"
        },
        {
            "name": "zscore(x)",
            "description": "Z-score cross-sectionally: (x - mean) / std"
        }
    ],
    "Vector": [
        {
            "name": "vec_avg(x)",
            "description": "Mean of vector field x"
        },
        {
            "name": "vec_sum(x)",
            "description": "Sum of vector field x"
        }
    ],
    "Transformational": [
        {
            "name": "bucket(rank(x), range='0,1,0.1' or buckets='2,5,6,7,10')",
            "description": "Convert float values into discrete bucket indexes"
        },
        {
            "name": "trade_when(x, y, z)",
            "description": "Only update alpha if condition is met, else hold or close position"
        }
    ],
    "Group": [
        {
            "name": "group_backfill(x, group, d, std=4.0)",
            "description": "Backfill NaN by winsorized mean of same group instruments in last d days"
        },
        {
            "name": "group_mean(x, weight, group)",
            "description": "All elements in a group => group mean"
        },
        {
            "name": "group_neutralize(x, group)",
            "description": "Neutralize alpha against group (industry, sector, etc.)"
        },
        {
            "name": "group_rank(x, group)",
            "description": "Rank each element within its group"
        },
        {
            "name": "group_zscore(x, group)",
            "description": "Z-score within each group: (x - mean) / std of that group"
        }
    ]
}

# In ra ví dụ
for category, funcs in OPERATORS.items():
    print(f"--- {category} ---")
    for f in funcs:
        print(f"  {f['name']}: {f['description']}")
    print()
