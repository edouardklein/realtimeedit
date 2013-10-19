(;;Real-Time Edit :
(defun write-buf-to-RTEFS ( localDir RTEdir )
  (message "write to buf called")
  (let ((fname (replace-regexp-in-string localDir RTEdir buffer-file-name)))
    ;(message (concat "idle file to be written : " fname))
    (if (file-writable-p fname)
	(write-region nil nil fname)
      ;(message (concat "File" (concat fname " is NOT writable, will try next time")))
      )
    )
  )

(defun launch-RTE ()
  "Launch the RTE"
  (interactive)
  (setq localDir default-directory)
  ;(message (concat "Launching RTE in directory :" localDir))
  (run-with-idle-timer 0.1 1 (lambda () (write-buf-to-RTEFS localDir "/tmp/mnt/input/")))
  ;(message "done")
  )

