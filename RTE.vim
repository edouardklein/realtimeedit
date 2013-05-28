au CursorHold * call UpdateFile()

let g:LocalDir='/home/edouard/Documents/relatimeedit/testLatex/'
let g:RTEdir='/tmp/mnt/input/'

function! UpdateFile()
	let l:cfname = expand('%:p')
	echom "idle is called on buffer ".l:cfname
	let l:fname = substitute(l:cfname, g:LocalDir,g:RTEdir, "")
	echom "file would be written in ".l:fname
	call writefile(getline(1,'$'), l:fname)
	echom "file has been written in ".l:fname
endfunction


