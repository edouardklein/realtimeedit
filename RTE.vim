let g:RTE_init=0

function! UpdateFile()
	if g:RTE_init==0
	    echom "Initialisation du plugin RTE"
	    au CursorHold * call UpdateFile()
	    au CursorHoldI * call UpdateFile()

	    let g:RTEdir='/tmp/mnt/input/'
	    let &ut=400
	    let g:RTE_init=1

	endif
	try
	    call writefile(getline(1,'$'), g:RTEdir.expand("%"))
	    "call writefile(getline(1,'$'), l:fname)
	catch /.*/
	endtry
	echom "file has been written in ".g:RTEdir.expand("%")
endfunction


