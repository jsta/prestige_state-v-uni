all: figures/lollipop.png

figures/lollipop.png: analysis.py
	python $<