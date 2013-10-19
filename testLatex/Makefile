RTEcompile:
	pdflatex -interaction=batchmode -halt-on-error main.tex

RTEstartView:
	PAPERSIZE=a4 xpdf -q -remote 'testRTE1' main.pdf

RTEview:
	PAPERSIZE=a4 xpdf -q -remote 'testRTE1' -reload

RTEstopView:
	xpdf -q -remote 'testRTE1' -quit

