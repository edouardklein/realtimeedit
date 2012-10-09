(defun write-buf-to-RTEFS ( localDir RTEdir )
  (let ((fname (replace-regexp-in-string localDir RTEdir buffer-file-name)))
    (message (concat "idle file to be written : " fname))
    (if (file-writable-p fname)
	(write-region nil nil fname)
      ;(message (concat "File" (concat fname " is NOT writable, will try next time")))
      )
    )
  )

(defun launch-RTE ()
  "Launch the RTE"
  (interactive)
  (message (concat "Launching RTE in directory :" default-directory))
  ;(sleep 1)
  (run-with-idle-timer 0.1 1 (lambda () (write-buf-to-RTEFS default-directory "/tmp/mnt/input/")))
  )


