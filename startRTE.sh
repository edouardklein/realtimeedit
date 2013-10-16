RTEFS.py /tmp/mnt 2>/dev/null & (nohup emacs Makefile --funcall launch-RTE  &); sleep 1
#RTEFS.py /tmp/mnt && (nohup gvim Makefile -c "call UpdateFile()" &); sleep 1
exit
