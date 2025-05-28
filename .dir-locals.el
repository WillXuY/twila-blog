((python-mode
  . ((eglot-server-programs . ((python-mode . ("~/.virtualenvs/twila-blog/bin/pylsp"))))
     (eval . (setenv "VIRTUAL_ENV" "~/.virtualenvs/twila-blog"))
     (eval . (let ((venv-bin "~/.virtualenvs/twila-blog/bin"))
               (unless (string-match-p (regexp-quote venv-bin) (getenv "PATH"))
                 (setenv "PATH" (concat venv-bin ":" (getenv "PATH")))))))))
