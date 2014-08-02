SCRIPTS  := $(filter-out _%.py, $(wildcard *.py))
PERF     := $(patsubst %.py, %.perf, $(SCRIPTS))
TIME     := $(patsubst %.py, %.time, $(SCRIPTS))
MEMIT    := $(patsubst %.py, %.memit, $(SCRIPTS))
KERNPROF := $(patsubst %.py, %.kernprof, $(SCRIPTS))

all: $(PERF) $(TIME) $(MEMIT) $(KERNPROF)

perf: $(PERF)

time: $(TIME)

memit: $(MEMIT)

kernprof: $(KERNPROF)

%.kernprof: %.py
	@echo "lineprof-izing $<"
	kernprof.py -l -v $< > $@ 2>&1

%.memit: %.py
	@echo "%memit-izing $<"
	python -m memory_profiler $< > $@ 2>&1

%.time: %.py
	@echo "Timing $<"
	time -v python $< > $@ 2>&1

%.perf: %.py
	@echo "Perfiling $<"
	#perf stat -B -e cache-references,cache-misses,cycles,instructions,branches,faults,migrations python $< > $@ 2>&1
	#perf stat -B -r 3 python $< > $@ 2>&1
	perf stat -e cycles,stalled-cycles-frontend,stalled-cycles-backend,instructions,cache-references,cache-misses,branches,branch-misses,task-clock,faults,minor-faults,cs,migrations -r 3 python $< > $@ 2>&1

clean:
	rm -rf $(PERF) $(TIME) $(MEMIT) $(KERNPROF)
