"""Phase 2 · NumPy · Arrays & indexing. Run: uv run --with numpy 01_numpy_arrays.py"""

# %% 1. Create arrays
import numpy as np

qty = np.array([120, 5000, 300, 800, 450])          # quantities of 5 orders
price = np.array([3.50, 0.04, 5.20, 0.30, 2.80])     # unit prices
print(qty, qty.dtype, qty.shape)
print(price, price.dtype)

# %% 2. A 2-D array: orders per weekday (rows = weeks, columns = Sat..Thu)
week_orders = np.array([
    [8, 15, 14, 16, 13, 15],
    [7, 14, 15, 12, 16, 14],
    [9, 16, 13, 15, 14, 17],
])
print(week_orders.shape, week_orders.ndim, week_orders.size)

# %% 3. Indexing and slicing
print(qty[0], qty[-1])          # first, last
print(qty[1:4])                 # positions 1, 2, 3
print(week_orders[1, 2])        # week 2, Mon
print(week_orders[:, 0])        # every Saturday
print(week_orders[0])           # week 1

# %% 4. Boolean masks: filter without loops
value = qty * price
print(value)
big = value >= 1000
print(big)
print(value[big])
print(qty[(price < 1) & (qty > 1000)])

# %% 5. Fancy indexing and sorting
order = np.argsort(value)[::-1]   # positions, biggest value first
print(order, value[order])

# %% 6. Reshape and stack
daily = np.arange(1, 13)
print(daily.reshape(3, 4))
print(np.vstack([qty, price]).shape)

# %% 7. Load columns from the practice file
data = np.genfromtxt("data/orders_2025.csv", delimiter=",", skip_header=1, usecols=(8, 9, 15))
print(data.shape)
print(data[:3])
np.set_printoptions(suppress=True)   # plain numbers instead of 4.6160e+03
print(data[:3])
revenue = data[:, 2]
print(f"Orders: {len(revenue)}, total revenue: {revenue.sum():,.2f}, largest: {revenue.max():,.2f}")

# %% Try it yourself — solution
print(week_orders.sum(axis=1))
days = np.array(["Sat", "Sun", "Mon", "Tue", "Wed", "Thu"])
print(days[(week_orders >= 16).any(axis=0)])
