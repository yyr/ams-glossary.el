;;; ams-glossary.el -- Read AMS glossary from Emacs

;; Copyright (C) 2012 Yagnesh Raghava Yakkala <http://yagnesh.org>

;; Author: Yagnesh Raghava Yakkala <yagnesh@live.com>
;; URL: https://github.com/yyr/ams-glossary.el
;; Maintainer: Yagnesh Raghava Yakkala <yagnesh@live.com>
;; Created: Sat Oct 20, 2012
;; Keywords: ncl, Major Mode, ncl-mode, atmospheric science.

;; This file is NOT part of GNU Emacs.

;; ncl-mode.el is free software: you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or
;; (at your option) any later version.

;; ncl-mode.el is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with this file.  If not, see <http://www.gnu.org/licenses/>.

;;; Commentary:
(defgroup ams-glossary nil
  "Client to accessing AMS Glossary site."
  :tag "ams-glossary"
  :group 'external)

(defcustom ag-site nil
  "The AMS Glossary site."
  :group 'ams-glossary)

(defcustom ag-cache-dir "~/.ams-glossary/"
  "Directory to store the cache."
  :group 'ams-glossary
  :type 'string)

(defun ag-retrieve-callback (status term &optional dest)
  (let* ((cdir (progn (unless (file-directory-p ag-cache-dir)
                        (make-directory ag-cache-dir))
                      (expand-file-name ag-cache-dir)))
         (dest (or dest (format "%s%s.htm" (file-name-as-directory cdir)
                                term)))
;         (part (concat dest ".part"))
         (buffer-file-coding-system 'no-conversion)
         (require-final-newline nil))
    ;; clean html header
    (goto-char (point-min))
    (re-search-forward "^$" nil 'move)
    (forward-char)
    (delete-region (point-min) (point))
    (write-file dest)))

(with-temp-buffer
  (url-retrieve "http://amsglossary.allenpress.com/glossary/search?id=water-mass1"
                'ag-retrieve-callback (list "term" "term")))

(defun ag-run-search (query)
  "Asks the user about query and searches, creates a new
  *ams-glossary* buffer and shows definitions in it."
  (interactive
   (ag-read-query (thing-at-point 'word)))
  (ag-run 'ag-search ))


(provide 'ams-glossary)
;;; ams-glossary.el ends here
