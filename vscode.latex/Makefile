build/main.pdf: source/main.tex
	latexmk -xelatex -synctex=-1 -interaction=nonstopmode -halt-on-error -outdir=build -auxdir=build source/main.tex

clean:
	rm -rf build
