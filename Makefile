DEST=~/bin

install:
	cp RTEFS.py $(DEST)/
	cp startRTE.sh $(DEST)/
	cp stopRTE.sh $(DEST)/
	cp RTEAgent.py $(DEST)/
#	cat RTE.el >> ~/.emacs #toupouri
	mkdir -p  ~/.vim/plugin
	cp RTE.vim ~/.vim/plugin
