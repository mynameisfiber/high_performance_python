```
$ python benchmark.py
Grid size:  (256, 256)
Pure Python: 1.22s (1.218498e-01s per iteration)
python+memory: 1.19s (1.186913e-01s per iteration)[1.03x speedup]
numpy: 0.02s (1.638103e-03s per iteration)[74.38x speedup]
numpy+memory: 0.01s (1.490402e-03s per iteration)[81.76x speedup]
numpy+memory2: 0.01s (7.136822e-04s per iteration)[170.73x speedup]
numpy+memory+scipy: 0.02s (1.522303e-03s per iteration)[80.04x speedup]

Grid size:  (512, 512)
Pure Python: 4.89s (4.889611e-01s per iteration)
python+memory: 4.64s (4.643779e-01s per iteration)[1.05x speedup]
numpy: 0.15s (1.469820e-02s per iteration)[33.27x speedup]
numpy+memory: 0.11s (1.104362e-02s per iteration)[44.28x speedup]
numpy+memory2: 0.04s (3.523612e-03s per iteration)[138.77x speedup]
numpy+memory+scipy: 0.08s (8.366203e-03s per iteration)[58.44x speedup]

Grid size:  (1024, 1024)
Pure Python: 20.76s (2.075953e+00s per iteration)
python+memory: 20.60s (2.059773e+00s per iteration)[1.01x speedup]
numpy: 0.55s (5.520298e-02s per iteration)[37.61x speedup]
numpy+memory: 0.40s (4.010251e-02s per iteration)[51.77x speedup]
numpy+memory2: 0.17s (1.718290e-02s per iteration)[120.82x speedup]
numpy+memory+scipy: 0.52s (5.219860e-02s per iteration)[39.77x speedup]
```
