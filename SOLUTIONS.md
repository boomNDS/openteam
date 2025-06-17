## Solution notes

### Task 01 – Run‑Length Encoder
- Language: Python
- Approach: like we count the number for each character if it match plus 1
if not match reset to 1 and store it in a list(string)
- Why:I start with the basic one that works before adjusting the solution, this solution only works for consecutive characters, it does not handle non-consecutive characters or characters that appear multiple times consecutively like (XYZXX) => (X3Y1Z1) OR (XYZXX) => (X1Y1Z1X2).
- Time spent: ~5 min
- **AI tools used:** [ZedAI](https://github.com/ZedAI) for autocompletion

### Task 02 – Fix‑the‑Bug (thread safety)
- Language: Python
- Approach: Find a solution form python doc and guide that use lock to ensure thread safety and how to use in module-level style
- Why: because on testing it call thread workers without some global variables that can be accessed by multiple threads simultaneously, leading to race conditions and incorrect results. found a doc how to handle it using lock
- Time spent: ~20 min
- **AI tools used:** [ZedAI](https://github.com/ZedAI) for autocompletion and ChatGPT (only focus on write a problem and let's it guide me to solve it)

### Task 03 – Sync Aggregator (concurrency & I/O)
- Language: Python
- Approach: [EXPLAIN YOUR ALGORITHM]
- Why: [TRADE-OFFS CONSIDERED]
- Time spent: ~15 min
- **AI tools used:** [ZedAI](https://github.com/ZedAI) for autocompletion

### Task 04 – SQL Reasoning (analytics & optimization)
- Language: Python
- Approach: [EXPLAIN YOUR ALGORITHM]
- Why: [TRADE-OFFS CONSIDERED]
- Time spent: ~20 min
- **AI tools used:** [ZedAI](https://github.com/ZedAI) for autocompletion
