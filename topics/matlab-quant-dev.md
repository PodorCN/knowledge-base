---
id: matlab-quant-dev
title: "MATLAB for Quant Developers (vs Python)"
type: topic
domain: quant-dev
sources: [src-rbc-gam-quantdev-notes]
---
# MATLAB for Quant Developers (vs Python)

Many asset-management teams keep their portfolio optimiser in MATLAB while data work moves to Python. This chapter teaches MATLAB to a Python programmer: the core differences and silent-bug traps, the syntax and containers, name-value arguments, calling Python from MATLAB and back, how the runtime executes code, how to write fast MATLAB, the pass-by-value memory model, MATLAB's object system, and how to handle constants and configuration in both languages.

**Prerequisites:** [[oop-pillars]] (classes and objects), [[eigen-svd-psd]] (matrix algebra).

**Leads to:** [[matlab-optimization-solvers]] (portfolio optimisation in MATLAB), [[production-coding]].

**Sections:** [[matlab-vs-python]] · [[matlab-syntax-basics]] · [[matlab-containers]] · [[matlab-name-value-arguments]] · [[matlab-python-interop]] · [[matlab-jit-multithreading]] · [[matlab-performance]] · [[matlab-memory-model]] · [[matlab-oop]] · [[globals-constants-config]]

Conventions of this chapter: **(sourced)** = from official documentation or cited pages; **(自己推理)** = own reasoning / general knowledge, not verified against a source. MATLAB snippets were **not executed** (no MATLAB available); Python snippets marked "measured" were run.

<a id="matlab-vs-python"></a>

## MATLAB vs Python — Core Differences
<!-- section: matlab-vs-python | prerequisites: [] | related: [matlab-syntax-basics, matlab-memory-model, csharp-refresher] | sources: [src-rbc-gam-quantdev-notes] | tags: [matlab, python, numpy, indexing] -->

MATLAB treats everything as a matrix, indexes from 1 and passes by value; Python/NumPy indexes from 0 and passes object references. Most porting bugs come from these differences being silent.

### Comparison

| Dimension | MATLAB | Python (NumPy/pandas) |
|---|---|---|
| Index start | **1** | 0 |
| Index syntax | `x(1)` | `x[0]` |
| Last element | `x(end)` | `x[-1]` |
| Slice | `x(2:5)` **includes** 5 | `x[1:5]` excludes 5 |
| Basic unit | Everything is a **matrix** (scalar = 1×1) | list / ndarray / DataFrame are separate |
| Matrix multiply | `A * B` | `A @ B` |
| Element-wise multiply | `A .* B` | `A * B` |
| Transpose | `A'` | `A.T` |
| Memory layout | Column-major | Row-major (default) |
| Block end | `end` | indentation |
| Comment | `%` | `#` |
| Trailing `;` | Suppresses output printing | n/a |
| Tabular data | `table` / `timetable` | `DataFrame` |
| Cost | Commercial, per-toolbox licences | Free / open source |
| Strength | Matrix math, Optimization/Financial toolboxes out of the box | Data engineering, ML, deployment ecosystem |

### Silent-bug traps when moving from Python (mostly 自己推理)

| Trap | Python | MATLAB |
|---|---|---|
| NaN in stats | pandas skips NaN | `mean([1 NaN 3])` = `NaN` → use `'omitnan'` |
| `std` denominator | `np.std` uses N | MATLAB `std` uses N−1 |
| Default reduction | explicit `axis` | `mean(X)` goes **down columns** |
| Vector orientation | 1-D has none | row (1×N) vs column (N×1) matters |
| Mutating inputs | NumPy in-place changes the caller | Never changes the caller (pass-by-value, [[matlab-memory-model]]) |
| Output noise | — | A missing `;` prints to the console |

### Why choose MATLAB over Python (mostly 自己推理; JIT/multithreading/toolboxes sourced)

| MATLAB advantages | Python advantages |
|---|---|
| Matrix-first syntax close to the math (`w'*Sigma*w`) | Free, open source |
| Officially maintained toolboxes (Optimization, Financial, Stats, Econometrics) | Data-engineering ecosystem (pandas, SQL, Databricks, cloud) |
| `Portfolio` object: constraints in one line ([[matlab-portfolio-object]]) | ML / deep learning |
| Vendor support helps model governance / audit | Easier hiring |
| Legacy core models already in MATLAB | Mature DevOps toolchain (pytest, CI/CD, Docker) |
| Integrated IDE, debugger, profiler, Live Scripts | |

**Interview answer:** "MATLAB's strength is concise, well-supported numerical and optimization code, which is why it often sits at the core of portfolio construction; Python's strength is the data and deployment ecosystem. I'd respect what already works in MATLAB and make the boundary between them clean and well-tested."

### Connections
- **Next:** [[matlab-syntax-basics]]. **Same exercise for C#:** [[csharp-refresher]].

<a id="matlab-syntax-basics"></a>

## MATLAB Syntax Crash Course
<!-- section: matlab-syntax-basics | prerequisites: [matlab-vs-python] | related: [matlab-containers, model-release-regression-testing] | sources: [src-rbc-gam-quantdev-notes] | tags: [matlab, syntax, vectorization, unit-test] -->

The MATLAB needed to read quant code: building vectors and matrices, indexing, matrix vs element-wise operations, statistics, control flow and functions, implicit expansion, and unit tests. Each line is paired with its NumPy equivalent.

### Vectors & matrices
```matlab
x = [1 2 3];          % row vector (1x3)
y = [1; 2; 3];        % column vector (3x1)
A = [1 2; 3 4];       % 2x2
I = eye(3);  Z = zeros(3,1);  o = ones(3,1);
n = numel(x);  [r, c] = size(A);
```

### Indexing
```matlab
A(1,2)     % row 1 col 2        ↔ A[0,1]
A(:,1)     % first column       ↔ A[:,0]
A(end,:)   % last row           ↔ A[-1,:]
x(x > 1)   % logical indexing   ↔ x[x > 1]
```

### Operations
```matlab
A * B      % matrix multiply    ↔ A @ B
A .* B     % element-wise       ↔ A * B
A ./ B     A .^ 2     A'
A \ b      % solve Ax = b (faster & more stable than inv(A)*b) ↔ np.linalg.solve
```

### Statistics
```matlab
mean(R)  std(R)  cov(R)  corr(R)     % column-wise (rows = dates, cols = assets)
mean(R, 'omitnan')
cumprod(1 + r)
```

### Control flow & functions
```matlab
for i = 1:10
    if x(i) > 0, disp(i);
    elseif x(i) == 0, continue;
    else, break;
    end
end

function [mu, sigma] = portStats(w, m, C)   % one file per function (file name = function name)
    mu = w' * m;
    sigma = sqrt(w' * C * w);
end

f = @(x) x.^2 + 1;                           % anonymous function ↔ lambda
```

### Implicit expansion (like NumPy broadcasting, R2016b+ — 自己推理)
```matlab
Z = (X - mean(X,2)) ./ std(X,0,2);   % cross-sectional z-score per row (date)
% mean(X,2): along rows → T×1;  std(X,0,2): 0 = N−1 denominator, along rows
```

### Unit testing
```matlab
% testPortStats.m
function tests = testPortStats
    tests = functiontests(localfunctions);
end
function testVol(testCase)
    [~, s] = portStats([1;0], [0.1;0.2], [0.04 0; 0 0.09]);
    verifyEqual(testCase, s, 0.2, 'AbsTol', 1e-12);
end
% runtests('testPortStats')   ↔ pytest
```

### Connections
- **Builds on:** [[matlab-vs-python]]. **Next:** [[matlab-containers]].
- **Testing in production:** [[model-release-regression-testing]].

<a id="matlab-containers"></a>

## Containers: Cell, Struct, Dictionary, Table
<!-- section: matlab-containers | prerequisites: [matlab-syntax-basics] | related: [matlab-python-interop, globals-constants-config] | sources: [src-rbc-gam-quantdev-notes] | tags: [matlab, cell-array, struct, dictionary, table] -->

**MATLAB has no "list".** The Python list corresponds to the **cell array** `{}`. Structs hold named fields, `dictionary` maps typed keys to typed values, and `table` is the DataFrame.

### Definitions

| MATLAB | Create | Holds | Python equivalent |
|---|---|---|---|
| Numeric array | `[1 2 3]` | Single type | ndarray |
| **Cell array** | `{1, 'AAPL', [1 2]}` | Any mixed types | **list** |
| String array | `["AAPL" "MSFT"]` | strings | list of str |
| Struct | `s.ticker = 'AAPL'` | Named fields | dict / dataclass |
| **dictionary** (R2022b+) | `dictionary(keys, vals)` | Typed key → value | dict |
| table | `readtable(...)` | Columns | DataFrame |

### `()` vs `{}` — the key rule
```matlab
c = {10, 'AAPL', [1 2 3]};
c(2)    % returns a 1x1 cell (the "box")   → {'AAPL'}
c{2}    % returns the contents              → 'AAPL'
```
Mental model: a cell array is a row of boxes; `()` takes the box, `{}` opens it.

`'AAPL'` is a char array (old); `"AAPL"` is a string (new, like a Python str).

### dictionary (sourced: MathWorks; introduced R2022b, recommended over `containers.Map`)
```matlab
d = dictionary(["AAPL" "MSFT" "RY"], [0.05 0.04 0.03]);   % string ⟼ double
d("TD") = 0.02;               % add
w = d("AAPL");                % lookup
d("TD") = [];                 % remove
keys(d); values(d); isKey(d,"RY"); numEntries(d); entries(d)   % entries → table
d = insert(d, "SHOP", 0.02);  d = remove(d, "SHOP");  lookup(d, "MSFT")
d = configureDictionary("string", "double");               % empty, typed
```

### Key points
- **All keys have the same type and all values have the same type** (unlike Python): `d("RY") = "high"` → error.
- Mixed values → use **cell** values; `info("AAPL")` returns the cell, `info{"AAPL"}` its contents.
- **Vectorised lookup:** `sectorCap(["Tech" "Financials" "Tech"])` → `[0.30 0.35 0.30]` (Python needs a list comprehension).

| Need | Use |
|---|---|
| ticker → one number | dictionary |
| Fixed-field config | struct |
| Many stocks × many fields | table |
| Pre-R2022b code | `containers.Map` |

### Connections
- **Builds on:** [[matlab-syntax-basics]].
- **Conversion to Python types:** [[matlab-python-interop]]. **Config as struct:** [[globals-constants-config]].

<a id="matlab-name-value-arguments"></a>

## Name-Value Arguments (MATLAB "parameters")
<!-- section: matlab-name-value-arguments | prerequisites: [matlab-syntax-basics] | related: [matlab-portfolio-object, matlab-optimization-solvers] | sources: [src-rbc-gam-quantdev-notes] | tags: [matlab, name-value, arguments-block, validation] -->

Name-value arguments are MATLAB's equivalent of Python keyword arguments (sourced: MathWorks). They are used by almost every toolbox function, and your own functions can declare them in an `arguments` block.

### Syntax
```matlab
Portfolio('AssetMean', mu, 'AssetCovar', Sigma)   % classic, all versions
Portfolio(AssetMean=mu, AssetCovar=Sigma)         % R2021a+
```

### Key points
- They must come **after** the positional arguments and can be in **any order**.
- Used everywhere:

```matlab
plot(x, y, 'LineWidth', 2)
opts = optimoptions('quadprog', 'Display', 'off');
T = readtable('prices.csv', 'Delimiter', ',');
p = estimateAssetMoments(p, R, 'DataFormat', 'Prices', 'MissingData', true);
```

### Defining your own (`arguments` block)
```matlab
function w = meanVarOpt(mu, Sigma, opts)
    arguments
        mu    (:,1) double
        Sigma (:,:) double
        opts.Lambda (1,1) double = 5       % name-value with default
        opts.MaxWeight (1,1) double = 1
    end
    n = numel(mu);
    w = quadprog(2*opts.Lambda*Sigma, -mu, [], [], ones(1,n), 1, zeros(n,1), opts.MaxWeight*ones(n,1));
end

w = meanVarOpt(mu, Sigma, 'MaxWeight', 0.4);
w = meanVarOpt(mu, Sigma, Lambda=10, MaxWeight=0.4);
```

(Size/type validation and defaults: 自己推理; older code uses `inputParser`.) Python equivalent: `def mean_var_opt(mu, Sigma, *, lam=5, max_weight=1)`.

### Connections
- **Builds on:** [[matlab-syntax-basics]].
- **Used by:** [[matlab-portfolio-object]] (`Portfolio('Name', value)`), [[matlab-optimization-solvers]] (`optimoptions`).

<a id="matlab-python-interop"></a>

## Calling Python from MATLAB (and vice versa)
<!-- section: matlab-python-interop | prerequisites: [matlab-containers] | related: [csharp-essentials, model-release-regression-testing] | sources: [src-rbc-gam-quantdev-notes] | tags: [matlab, python, interop, pyrunfile, engine-api] -->

MATLAB can call Python in three ways — the `py.` prefix, `pyrun` and `pyrunfile` — and Python can drive MATLAB through the MATLAB Engine API. For production, Python should be packaged as a module with a clear function interface.

### Setup
```matlab
pe = pyenv;                       % inspect current interpreter
pyenv("Version", "3.11");         % set BEFORE first py. call; to change later: restart (InProcess) or terminate (OutOfProcess)
```

### Method 1 — `py.` prefix (recommended for production)
```matlab
x   = py.math.sqrt(42);
arr = py.numpy.array([1 2 3]);
z   = py.signals.compute_zscore(arr);            % your own module signals.py
py.mymod.foo(5, pyargs('bar', 42));             % Python keyword args
py.importlib.reload(py.importlib.import_module('signals'));   % after editing .py
```

### Method 2 — `pyrun` (a few lines as a string; variables PERSIST between calls)
```matlab
x = pyrun("a = b*c", "a", b=5, c=10)   % x = 50
```

| Step | What happens |
|---|---|
| `b=5, c=10` | Create Python variables b, c |
| `"a = b*c"` | Execute in Python → a = 50 |
| `"a"` | Tell MATLAB which Python variable to return (the name must match exactly) |
| `x = ...` | Store in MATLAB variable x (names are independent) |

```matlab
pyrun("k = 3");
y = pyrun("z = k * 2", "z")     % y = 6, k still exists
```

### Method 3 — `pyrunfile` (run a .py file; R2021b+; variables do NOT persist)
Syntax (sourced): `pyrunfile(file)`, `pyrunfile("file.py arg")` (argv as **strings**), `outvars = pyrunfile(file, outputs, pyName=pyValue)`.

**backtest.py**
```python
import numpy as np
rets = np.asarray(rets, dtype=float)          # rets INJECTED by MATLAB
nav = np.cumprod(1 + rets)
total_return = float(nav[-1] - 1)
max_dd = float((nav / np.maximum.accumulate(nav) - 1).min())
```

**test_backtest.m**
```matlab
myRets = [0.01 -0.02 0.03 0.01];
[tr, dd] = pyrunfile("backtest.py", ["total_return" "max_dd"], rets = myRets);
% tr = 0.0297 (2.97%), dd = -0.0200 (-2.00%)   [verified on Python side]
```

Data flow:
```
MATLAB myRets ──rets=──► Python rets
Python total_return ──"total_return"──► MATLAB tr
Python max_dd ───────"max_dd"────────► MATLAB dd
```

- **Why no NameError?** `rets=myRets` injects `rets` into the script namespace *before* execution. The official example `addac.py` does `z = add(x,y)` with x, y never defined in the file.
- **But** running `python backtest.py` standalone → `NameError: name 'rets' is not defined` (verified). Linters flag it, and it can't be unit-tested.
- **Pitfalls:** output names must match; the number of left-hand outputs must equal the number of names; the `pyrunfile` namespace is discarded after each call.

### Better: module + function
```python
# backtest.py
import numpy as np
def run_backtest(rets):
    rets = np.asarray(rets, dtype=float)
    nav = np.cumprod(1 + rets)
    return float(nav[-1] - 1), float((nav / np.maximum.accumulate(nav) - 1).min())

if __name__ == "__main__":
    print(run_backtest([0.01, -0.02, 0.03, 0.01]))
```
```matlab
res = py.backtest.run_backtest(myRets);   % returns tuple
tr = double(res{1});  dd = double(res{2});
```

### Type conversion

| MATLAB → Python | |
|---|---|
| double/single | float (arrays → NumPy array when NumPy is available, R2025a+) |
| int types | int |
| NaN / Inf | float nan / inf |
| string/char | str |
| logical | bool |
| struct / dictionary | dict |
| **table** | **pandas DataFrame** |
| datetime | datetime.datetime |

Python → MATLAB: NumPy array → `double(x)`; DataFrame → `table(df)`; tuple/list elements → `res{1}`.

### Worked example: MATLAB prices → Python signals → MATLAB optimizer
```matlab
[alphaPy, covPy, summaryPy] = pyrunfile("compute_signals.py", ["alpha" "cov" "summary"], ...
    prices = prices, lookback = int32(60));
alpha   = double(alphaPy)';      % 1xN → Nx1
Sigma   = double(covPy);
summary = table(summaryPy);
w = quadprog(2*5*Sigma, -alpha, [], [], ones(1,N), 1, zeros(N,1), 0.4*ones(N,1));
```

### Reverse: Python calls MATLAB
```python
import matlab.engine
eng = matlab.engine.start_matlab()
w = eng.my_optimizer(alpha, Sigma)
eng.quit()
```

**Interview answer:** "For quick scripts I'd use `pyrunfile`, but in production I'd package Python as a module with a clear function interface, unit-test it in Python, call it with `py.module.func()`, and put a regression test at the MATLAB boundary."

**References:**

- MathWorks: [Call Python from MATLAB](https://www.mathworks.com/help/matlab/call-python-libraries.html) · [pyrunfile](https://www.mathworks.com/help/matlab/ref/pyrunfile.html) · [pyenv](https://mathworks.com/help/matlab/ref/pyenv.html) · [Calling Python from MATLAB cheat sheet](https://www.mathworks.com/content/dam/mathworks/fact-sheet/calling-python-from-matlab-cheat-sheet.pdf) · [Python data types in MATLAB](https://www.mathworks.com/help/matlab/python-data-types.html) · [Use pandas DataFrames in MATLAB](https://www.mathworks.com/help/matlab/matlab_external/python-pandas-dataframes.html) · [Handle data returned from Python](https://uk.mathworks.com/help/matlab/matlab_external/handle-data-returned-from-python-function.html)

### Connections
- **Builds on:** [[matlab-containers]] (types being converted).
- **Same problem in C#:** C++ interop in [[csharp-essentials]]. **Boundary tests:** [[model-release-regression-testing]].

<a id="matlab-jit-multithreading"></a>

## Runtime: JIT & Multithreading
<!-- section: matlab-jit-multithreading | prerequisites: [matlab-syntax-basics] | related: [matlab-performance, dotnet-concurrency-wpf] | sources: [src-rbc-gam-quantdev-notes] | tags: [matlab, jit, multithreading, parfor] -->

MATLAB is dynamically typed like Python but JIT-compiles all code, so loops are much cheaper than in pure Python. Built-in functions are multithreaded automatically; your own loops are not.

### Definition: JIT (just-in-time compilation)
Code is compiled to machine code **at run time**, and the compiled result is cached.

| Mode | Analogy | Example | Speed |
|---|---|---|---|
| AOT (ahead-of-time) | Whole book translated before publishing | C++ | Fastest; recompile after changes |
| Interpreted | Simultaneous interpreter, re-translates every time | CPython | Slowest (loops) |
| **JIT** | Translate while reading, keep notes for next time | MATLAB, Java, Julia | Middle |

### Key points
- (sourced) MATLAB's execution engine (R2015b) JIT-compiles **all** MATLAB code; many core functions are **implicitly multithreaded**.
- The MATLAB runtime is **closer to Python** (dynamic typing, no compile step), but loops are much cheaper than in pure Python.

### Multithreading

| Level | What | Needs |
|---|---|---|
| **Implicit** | Built-ins (`*`, `\`, `sum`, `sort`, element-wise math) use multiple cores automatically | Nothing (sourced) |
| `parfor` | Parallel independent loop iterations | Parallel Computing Toolbox (自己推理) |
| `parfeval` + `backgroundPool` | Asynchronous function execution | Mentioned in the MathWorks performance guide |
| `parpool("Threads"/"Processes")`, GPU arrays | Worker pools / GPU | Parallel Computing Toolbox (自己推理) |

Your own `for` loop runs on **one thread** (like Python with the GIL, where NumPy's BLAS is multithreaded but Python loops aren't).

```matlab
parfor k = 1:nDates
    W(:,k) = optimizeWeights(alpha(:,k), SigmaCell{k}, cfg);
end
```

**References:**

- MathWorks: [MATLAB performance (JIT)](https://uk.mathworks.com/products/matlab/performance.html) · [MATLAB acceleration](https://uk.mathworks.com/discovery/matlab-acceleration.html) · MATLAB Answers: [JIT R2015b](https://www.mathworks.com/matlabcentral/answers/239817-matlab-s-r2015b-new-jit-experiences-a-severe-degradation-in-speed-in-the-following-example-but-the)

### Connections
- **Builds on:** [[matlab-syntax-basics]]. **Next:** [[matlab-performance]].
- **Same distinction in .NET:** I/O-bound vs CPU-bound work in [[dotnet-concurrency-wpf]].

<a id="matlab-performance"></a>

## Writing Efficient MATLAB
<!-- section: matlab-performance | prerequisites: [matlab-jit-multithreading] | related: [matlab-memory-model, globals-constants-config, monte-carlo-pricing] | sources: [src-rbc-gam-quantdev-notes] | tags: [matlab, performance, vectorization, preallocation, profiling] -->

MathWorks' own recommendations: profile first, then use functions rather than scripts, preallocate, vectorise, and avoid globals and `eval`.

### Official MathWorks list (sourced)
- **Functions over scripts** ("Functions are generally faster"); local > nested functions; modular code.
- **Preallocate** arrays; **vectorize**; move loop-invariant work outside loops.
- Don't change a variable's class/shape — create a new variable.
- Use short-circuit `&&` `||`.
- **Avoid global variables** ("Global variables diminish performance", [[globals-constants-config]]).
- Don't overload built-ins; avoid "data as code".
- Avoid `eval/evalin` (use function handles + `feval`); avoid `clear all`, `cd`, `addpath`, `exist`, `which` in running code.
- Background / parallel / GPU where appropriate ([[matlab-jit-multithreading]]).

### Profile first
```matlab
profile on; runBacktest(); profile viewer
t = timeit(@() runBacktest());
```

### Vectorize
```matlab
% slow
for t = 1:T, for i = 1:N, port(t) = port(t) + R(t,i)*w(i); end, end
% fast
port = R * w;
nav  = cumprod(1 + port);
```

### Preallocation — what & why
Create the array at its final size **before** filling it. Growing it (`x(end+1) = v`) reallocates and copies each time → O(n²).

```matlab
x = zeros(50000, 1);
for i = 1:50000, x(i) = i*0.5; end
```

**Not MATLAB-only:**

| Language | Slow | Fast |
|---|---|---|
| MATLAB | `x(end+1)=v` | `zeros(n,1)` |
| NumPy | `np.append` | `np.zeros(n)` |
| C++ | `push_back` without reserve | `reserve(n)` |

**Example:** measured (NumPy, n = 50,000): `np.append` **1.86 s** vs preallocated **0.005 s** → ~**366×**. Python's `list.append` over-allocates (amortised O(1)) — that's why Python users rarely notice.

### Why functions beat scripts
- Sourced: "Functions are generally faster"; MathWorks staff: R2015b runs code faster as a function than as a script.
- Mechanism (自己推理): scripts run in the shared base workspace (any variable may change) → the JIT can't assume types; functions have a private workspace → more optimisation, and they are testable.

### Other tips (自己推理)
- Column-major: store assets as columns; `R(:,i)` is contiguous.
- `x = f(x)` inside functions enables in-place optimisation ([[matlab-memory-model]]).
- Numeric matrices are fastest; extract from `table` before tight loops.
- Build `optimoptions` once, outside rebalance loops.
- In OOP code: **copy properties into locals** inside hot loops, write back once ([[matlab-oop]]).

**References:**

- MathWorks: [Techniques to improve performance](https://www.mathworks.com/help/matlab/matlab_prog/techniques-for-improving-performance.html)

### Connections
- **Builds on:** [[matlab-jit-multithreading]].
- **Related:** [[matlab-memory-model]], [[globals-constants-config]]; hot-loop allocation in .NET Monte Carlo ([[monte-carlo-pricing]]).

<a id="matlab-memory-model"></a>

## Memory Model: Pass-by-Value, Copy-on-Write, Handle Objects
<!-- section: matlab-memory-model | prerequisites: [matlab-performance] | related: [matlab-oop, matlab-vs-python, csharp-essentials] | sources: [src-rbc-gam-quantdev-notes] | tags: [matlab, pass-by-value, copy-on-write, handle, in-place] -->

MATLAB semantically passes every variable by value, implemented with copy-on-write so that passing a large matrix is cheap unless the function modifies it. Handle classes are the exception: the handle is copied but the object is shared. This is the opposite of NumPy, where a function that mutates its argument changes the caller's data.

### Pass-by-value (sourced — very likely interview question)
- "**MATLAB passes all variables by value.**" (Comparison of MATLAB and Other OO Languages)
- "When calling a function with input arguments, MATLAB copies the values from the calling function's workspace into the parameter variables..." (Avoid Unnecessary Copies of Data)
- **Copy-on-write:** "If a function does not modify an input argument, MATLAB does not make a copy."

```matlab
function Y = f1(X)
    Y = X .* 1.1;      % X only READ → shares A's memory, no copy
end
function Y = f2(X)
    X = X .* 1.1;      % X WRITTEN → independent copy made
    Y = X;
end
```
The caller's `A` is unchanged in both cases.

### In-place optimisation (sourced)
```matlab
function canBeOptimized
    A = rand(1e7,1);
    A = fLocal(A);          % same variable in and out
end
function X = fLocal(X)
    X = X .* 1.1;           % done in place, no new allocation
end
```
Conditions: the `A = f(A)` pattern; inside a function (not a script, the command line, `eval` or `try-catch`); no indexed assignment in a loop (e.g. `X{i} = ...` fails); the variable is not `global`/`persistent`.

### Handle objects (sourced)
- A class that inherits from `handle`: `classdef Book < handle`.
- "All copies of a handle object variable refer to the same underlying object."
- Passing it to a function "copies only the handle, not the object."
- Analogy: value object = photocopy; handle object = shared Google Doc link.

```matlab
function addCash(b), b.Cash = b.Cash + 100; end   % caller sees it (handle)
function replaceBook(b), b = Book; b.Cash = 999; end % rebinding local handle → caller unaffected (自己推理)
```

### Worked example: value vs handle — four scenarios
```matlab
classdef ValAccount                      classdef HAccount < handle
    properties, Cash = 0, end                properties, Cash = 0, end
    methods                                  methods
      function deposit(obj,x)                  function deposit(obj,x)
        obj.Cash = obj.Cash + x;                 obj.Cash = obj.Cash + x;
      end                                      end
      function obj = depositR(obj,x)           function obj = depositR(obj,x)
        obj.Cash = obj.Cash + x;                 obj.Cash = obj.Cash + x;
      end                                      end
    end                                      end
end                                      end
```

| | No return `obj.f(x)` | Return `obj = obj.f(x)` |
|---|---|---|
| **Value class** | ❌ 0 — change lost silently | ✅ 100 |
| **Handle class** | ✅ 100 | ✅ 100 (return redundant; same object) |

Copies: `v2 = v1` → independent; `h2 = h1` → the same object.

### Is `f(x)` with no output an in-place modification?
**No.** It depends on the **type**, not the call syntax:

- Value types (arrays, structs, tables, cells, `Portfolio`) → changes made by `f(x)` are lost; you must use `x = f(x)`.
- Handle objects → `f(obj)` modifies the shared object.

Two meanings of "in-place": **semantic** (the caller sees the change — only handles) vs **memory** (no new allocation — the `A = f(A)` optimisation).

### Python contrast (自己推理)

| | Python/NumPy | MATLAB normal arrays | MATLAB handle |
|---|---|---|---|
| Model | Pass by object reference | By value (copy-on-write) | Handle copied, object shared |
| Function mutates input | **Caller sees it** | Caller doesn't | Caller sees it |
| Function rebinds param | Caller unaffected | Unaffected | Unaffected |

```python
def normalize(w): w /= w.sum()        # Python: caller's array normalized
```
```matlab
function normalize(w), w = w/sum(w); end   % MATLAB: nothing happens to caller
weights = normalize2(weights);             % correct: return & reassign
```

### When to use value vs handle

| Value class | Handle class |
|---|---|
| Data: trades, weights, configs, optimisation problems | Entities with identity/shared state: DB connection, logger, live order book, GUI |
| `Portfolio`, `datetime`, `table` | Graphics objects, `containers.Map` |

### Why have no-return functions?
A function either **computes** (return the result) or **does** (a side effect):

- Output: `plot`, `disp`, `fprintf`, `writetable`.
- Logging/audit; validation (`validateConfig` throws on error); modifying handle objects; tests.
- Trap: a no-return function whose only purpose is modifying a value-type input → useless.
- Rule (自己推理): keep core math **pure** (inputs → outputs); reserve no-return functions for side effects.

**Interview answer:** "Semantically MATLAB passes by value — the docs say it passes all variables by value — implemented with copy-on-write, so passing a large matrix is cheap unless the function modifies it; even then `A = f(A)` inside functions can be optimized in place. The exception is handle classes: the handle is copied but refers to the same object, so property changes are visible to the caller. That's the opposite of NumPy, where in-place mutation in a function affects the caller — a common silent bug when porting Python code."

**References:**

- MathWorks: [Avoid unnecessary copies of data](https://www.mathworks.com/help/matlab/matlab_prog/avoid-unnecessary-copies-of-data.html) · [Comparison of handle and value classes](https://www.mathworks.com/help/matlab/matlab_oop/comparing-handle-and-value-classes.html) · [Handle object behavior](https://www.mathworks.com/help/matlab/matlab_oop/handle-objects.html)

### Connections
- **Builds on:** [[matlab-performance]] (in-place optimisation).
- **Used by:** [[matlab-oop]] (value vs handle classes), [[matlab-portfolio-object]] (a value object: always reassign).
- **Contrast:** value vs reference types in C# ([[csharp-essentials]]).

<a id="matlab-oop"></a>

## MATLAB OOP — How It Works & Why It's Unpopular
<!-- section: matlab-oop | prerequisites: [matlab-memory-model, oop-pillars] | related: [csharp-abstract-classes, matlab-performance] | sources: [src-rbc-gam-quantdev-notes] | tags: [matlab, oop, classdef, handle, performance] -->

MATLAB classes default to value semantics, pass the object explicitly, and historically carried a large overhead on property access and method calls. That, plus file-layout friction, is why most MATLAB quant code is written as functions on matrices.

### Minimal class
```matlab
% Strategy.m
classdef Strategy
    properties
        Name
        Lambda = 5
    end
    methods
        function obj = Strategy(name, lambda)       % constructor ↔ __init__
            obj.Name = name;  obj.Lambda = lambda;
        end
        function w = optimize(obj, alpha, Sigma)     % obj passed explicitly ↔ self
            n = numel(alpha);
            w = quadprog(2*obj.Lambda*Sigma, -alpha, [], [], ones(1,n), 1, zeros(n,1), ones(n,1));
        end
    end
end
s = Strategy("LowVol", 10);  w = s.optimize(alpha, Sigma);   % or optimize(s, alpha, Sigma)
```

### Differences vs other OO languages (sourced: MathWorks comparison page)

| Point | MATLAB | Python |
|---|---|---|
| Default semantics | **Value class** (copy on assign) | Reference |
| Reference semantics | `< handle` | default |
| Object parameter | Explicit `obj` | `self` (also explicit) |
| Superclass call | `method@SuperClass(obj)` | `super().method()` |
| Overloading by signature | Not supported | Not supported |
| Dispatch | Leftmost object argument | — |
| Templates/generics | None | — |
| Static properties | Not supported → `Constant` or `persistent` | Class variables |

### Why MATLAB OOP is considered painful — concrete examples
**A. Value-class lost update**
```matlab
a = Account;  a.deposit(100);  disp(a.Cash)   % 0 !! no error
```

**B. Handle-class aliasing surprise**
```matlab
portB = portA;  portB.Positions(1) = 0;   % portA changed too!
% true copy needs matlab.mixin.Copyable + copy()  (自己推理)
```

**C. Performance overhead (sourced: MATLAB Answers)**

| Same operation as… | Throughput |
|---|---|
| Workspace variables | ~42,000 kOps/s |
| Property access | ~2,800 kOps/s (~15× slower) |
| Method calls | ~1,700 kOps/s (~24× slower) |
| Static methods | ~8 kOps/s |

2011 benchmark: 100k method calls — handle 3.3 s vs non-OOP 0.025 s. The gap narrowed a lot in R2015b/R2018a/R2020a, but the reputation stuck. Fix: copy properties to locals in hot loops ([[matlab-performance]]).

**D. Developer friction (自己推理):** one class per file; `@Class` / `+package` folders; editing a class often needs `clear classes`; verbose `properties/methods/end`; the user base (engineers/researchers) writes scripts; matrix-in/matrix-out code rarely needs classes.

### Key points
- Where OOP still pays off: stable, reusable components with a common interface (e.g. a `Signal` base class with `compute()`), data-source wrappers.

**References:**

- MathWorks: [Comparison of MATLAB and other OO languages](https://www.mathworks.com/help/matlab/matlab_oop/matlab-vs-other-oo-languages.html) · [classdef](https://www.mathworks.com/help/matlab/ref/classdef.html) · MATLAB Answers: [class property slowness](https://www.mathworks.com/matlabcentral/answers/552916-numerical-operations-are-slow-on-class-properties-versus-in-workspace) · [OOP handle vs value vs no OOP](https://www.mathworks.com/matlabcentral/answers/15533-object-oriented-programming-performance-comparison-handle-class-vs-value-class-vs-no-oop)

### Connections
- **Builds on:** [[matlab-memory-model]], [[oop-pillars]].
- **Contrast:** C# classes in [[csharp-abstract-classes]].

<a id="globals-constants-config"></a>

## Global Variables, Constants & Config Files (MATLAB & Python)
<!-- section: globals-constants-config | prerequisites: [matlab-performance, matlab-containers] | related: [matlab-memory-model, pricing-app-architecture] | sources: [src-rbc-gam-quantdev-notes] | tags: [globals, constants, config, json, toml, persistent, lru-cache] -->

Global variables slow MATLAB down and create hidden dependencies in both languages. The engineering answer is to separate true constants (in code), configuration (a version-controlled file loaded and passed explicitly) and secrets (environment variables).

### MATLAB globals hurt performance (sourced)
- "Global variables diminish performance." (MathWorks performance guide)
- In-place optimisation is **not applied** to `global`/`persistent` variables ([[matlab-memory-model]]).
- MATLAB Answers: with globals, MATLAB must search beyond the current workspace and the Accelerator can't optimise the call; passing arguments is already cheap because of copy-on-write.
- Horror story: ~250 scalar globals declared in a **script** called in a 1000-iteration loop — 6 s (R2012b) → 67 s (R2017a) → 320 s (R2020b); fixed by a single struct (the root cause was largely the script + loop; MathWorks couldn't reproduce it).
- Historically (~2010) globals were sometimes faster for recursion; no longer.

### Python globals (measured + sourced)
- A local is `LOAD_FAST` (an array slot); a global is `LOAD_GLOBAL` (a dict lookup, then builtins).
- Python 3.11 (PEP 659) caches global lookups: "Loading globals and builtins require zero namespace lookups."
- **Measured (Python 3.11, 1M-iteration loop): global 0.161 s vs local 0.153 s → ~6% slower.**
- Bigger trap (自己推理): module-level (top-level script) code uses globals for *all* variables → put loops in functions. For numerics, vectorise anyway.
- Real reasons to avoid globals: hidden dependencies, silent mutation of global dicts/lists, test leakage, threading.

| | MATLAB | Python 3.11+ |
|---|---|---|
| Global access cost | "Diminish performance"; blocks in-place optimisation | Small (~6% in the test above) |
| Top-level code slower | Yes (scripts) | Yes (module-level globals) |
| Enforced constants | `properties (Constant)` | Convention; `Final` checked by the type checker only |

### Three kinds of "global" values (自己推理 / engineering practice)

| Kind | Example | Where |
|---|---|---|
| True constants | 252 trading days, bps conversion | Code, immutable |
| Configuration | λ, max weight, turnover, paths | Version-controlled config file, loaded at the entry point, passed explicitly |
| Secrets | DB passwords, API keys | Env vars / secrets manager — never in git |

### MATLAB constants (sourced)
```matlab
% +quant/Const.m
classdef Const
    properties (Constant)
        TRADING_DAYS = 252
        RISK_FREE    = 0.03
        DAILY_RF     = quant.Const.RISK_FREE / quant.Const.TRADING_DAYS
    end
end
annVol = dailyVol * sqrt(quant.Const.TRADING_DAYS);
quant.Const.TRADING_DAYS = 250;   % ❌ error
```
- Immutable; accessed as `Class.Prop` without an instance; evaluated **once at class load** (e.g. `RN = rand(5)` stays fixed until the class is cleared); namespaced via `+package`.
- Caveat: a constant holding a handle object — the object's properties can still change.
- The built-ins `pi`, `eps`, `i`, `j` are **functions** and can be shadowed: `pi = 3;` → silent bugs; `clear pi`. Use `1i` for the imaginary unit. (自己推理)

### Shared mutable state (not a true constant) — preference order (自己推理)

| Option | MATLAB | Python |
|---|---|---|
| ① Pass explicitly (default) | `optimize(alpha, Sigma, ctx)` | same |
| ② Context/state object | handle class | class instance / dataclass |
| ③ Load-once cache | `persistent` variable | `functools.lru_cache` |
| ④ True global | `global` (avoid) | module variable (avoid) |

```matlab
function S = riskModel()
    persistent cache
    if isempty(cache), cache = load("risk_model.mat"); end
    S = cache;
end
```
```python
from functools import lru_cache
@lru_cache(maxsize=1)
def risk_model(): return load_risk_model("risk_model.parquet")
```

### Config files — MATLAB

| Format | Function | Since | Result |
|---|---|---|---|
| JSON | `jsondecode(fileread("cfg.json"))` | R2016b | struct |
| JSON/XML | `readstruct("cfg.json")` | JSON since R2023b | struct |
| CSV/Excel | `readtable` | — | table |
| MAT | `load("cfg.mat")` | — | struct |
| Env var | `getenv("DB_PASSWORD")` | — | char |
| YAML/TOML | Not built in (as far as I know) | — | — |

JSON mapping (sourced): object → struct; number → double; bool → logical; string → char; homogeneous array → typed array; mixed → cell ([[matlab-containers]]).

```matlab
function main()
    cfg = jsondecode(fileread("strategy.json"));
    validateConfig(cfg);
    w = optimizeWeights(alpha, Sigma, cfg);
end
function validateConfig(cfg)
    assert(cfg.lambda > 0, "lambda must be positive");
end
```

### Config files — Python
```python
import tomllib                      # stdlib since 3.11, read-only, open in "rb"
from dataclasses import dataclass
from typing import Final

TRADING_DAYS: Final = 252

@dataclass(frozen=True)
class StrategyConfig:
    lambda_: float
    max_weight: float

with open("strategy.toml", "rb") as f:
    d = tomllib.load(f)
cfg = StrategyConfig(d["lambda"], d["max_weight"])
```
Also: `json` (stdlib), `yaml.safe_load` (pyyaml), `pydantic-settings` for validated config + env overrides.

**Mixed stack (自己推理):** one **JSON** file as the single source of truth — MATLAB `jsondecode`, Python `json` — avoids "λ = 5 in MATLAB, 4 in Python" drift; keep it in git.

**References:**

- MathWorks: [Constant properties](https://www.mathworks.com/help/matlab/matlab_oop/properties-with-constant-values.html) · [jsondecode](https://www.mathworks.com/help/matlab/ref/jsondecode.html) · [readstruct](https://www.mathworks.com/help/matlab/ref/readstruct.html) · MATLAB Answers: [globals fast?](https://www.mathworks.com/matlabcentral/answers/349193-global-variables-are-fast-functions-make-copies-or-not) · [globals inefficient](https://www.mathworks.com/matlabcentral/answers/1639475-why-has-matlab-become-extremely-inefficient-with-global-variables)
- Python: [What's new in Python 3.11 (PEP 659)](https://docs.python.org/3/whatsnew/3.11.html) · [tomllib](https://docs.python.org/3/library/tomllib.html)

### Connections
- **Builds on:** [[matlab-performance]], [[matlab-containers]].
- **Same principle:** immutable market-data snapshots and explicit inputs in [[pricing-app-architecture]].
