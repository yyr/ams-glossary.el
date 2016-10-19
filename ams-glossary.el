;;; ams-glossary.el -- Read AMS glossary from Emacs

;; Copyright (C) 2012, 2015, 2016 Yagnesh Raghava Yakkala <http://yagnesh.org>

;; Author: Yagnesh Raghava Yakkala <yagnesh@live.com>
;; Package-Requires: ((s))
;; Version: 0.1
;; URL: https://github.com/yyr/ams-glossary.el
;; Maintainer: Yagnesh Raghava Yakkala <yagnesh@live.com>
;; Created: Sat Oct 20, 2012
;; Keywords: AMS, Major Mode, ams-glossary, atmospheric science.

;; This file is NOT part of GNU Emacs.

;; ams-glossary.el is free software: you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or
;; (at your option) any later version.

;; ams-glossary.el is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with this file.  If not, see <http://www.gnu.org/licenses/>.

;;; Commentary:
;;

;;; Code:

(require 's)
(require 'ag-titles)

(defgroup ams-glossary nil
  "Client to accessing AMS Glossary site."
  :tag "ams-glossary"
  :group 'external)

(defcustom ag-site nil
  "The AMS Glossary site."
  :group 'ams-glossary)

(defvar ag-dir (file-name-directory
                        (or load-file-name buffer-file-name)))

(defconst ag-home-url "http://glossary.ametsoc.org/")
(defconst ag-term-url-template "http://glossary.ametsoc.org/wiki/%s")


(defcustom ag-cache-dir "~/.ams-glossary/"
  "Directory to store the cache."
  :group 'ams-glossary
  :type 'string)

(defvar ag-sample-term "oasis effect")

(defun ag-term-sanitize (term)
  (s-replace " " "_" term))

(defun ag-construct-url (term)
  (format ag-term-url-template (s-capitalize (ag-term-sanitize term))))

(defun ag-browse-term (term)
  (browse-url (ag-construct-url term)))

;;; search terms
;;; ---------------------------
(defvar ag-search-buffer-name
  "*AMS Glossary Search")

(defvar ag-search-return-window-config nil
  "Previous window config.")

(defvar ag-search-mode-map
  (let ((map (make-sparse-keymap)))
    (define-key map "\C-m"     'ag-search-browse-url)
    (define-key map " "        'ag-search-browse-url)
    (define-key map "q"        'ag-search-quit-window)
    (define-key map "Q"        'ag-search-exit-window)
    (define-key map "n"        'ag-search-move-next-line)
    (define-key map "p"        'ag-search-move-prev-line)

    (define-key map "/"        'isearch-forward)
    (define-key map "l"        'recenter)
    (define-key map "<"        'beginning-of-buffer)
    (define-key map ">"        'end-of-buffer)
    (define-key map "v"        'scroll-down)
    map)
  "Keymap for `ag-search-mode'.")

(define-derived-mode ag-search-mode fundamental-mode "ag-search"
  "major mode to list search results of AMS glossary titles."
  :group 'ams-glossary
  (kill-all-local-variables)
  (setq mode-name "ag-search")
  (use-local-map ag-search-mode-map)
  (setq buffer-read-only t)
  (run-mode-hooks))

(defun ag-search-term (word)
  (remove nil (mapcar (lambda (x)
                        (if (string-match word x)
                            x))
                      ag-title-list)))

(defun ag-search-browse-url ()
  (interactive)
  (let ((term  (buffer-substring-no-properties
                (line-beginning-position) (line-end-position))))
    (ag-browse-term term)))

(defun ag-search-list-term (word)
  (interactive (list
                (funcall #'completing-read "Title: " ag-title-list)))
  (let ((results (ag-search-term word))
        (cur-window-conf (current-window-configuration))
        (tmpbuf (get-buffer-create ag-search-buffer-name)))
    (display-buffer tmpbuf)
    (pop-to-buffer tmpbuf)
    (setq buffer-read-only nil)
    (erase-buffer)

    ;;
    (insert (format "#### Number of Matched AMS Titles: %s\n\n" (length results)))

    ;; insert list
    (mapc (lambda (x)
            (insert (format "%s\n" x)))
          results)
    (goto-char (point-min))
    (forward-line (1- 3))
    (ag-search-mode)
    (font-lock-add-keywords
     nil `((,(format "\\(%s\\|%s\\|%s\\)"
                     word
                     (upcase word)
                     (upcase-initials word))
            1
            font-lock-warning-face prepend)))
    (set (make-local-variable 'ag-search-return-window-config)
         cur-window-conf)
    (shrink-window-if-larger-than-buffer (get-buffer-window tmpbuf))))


(defun ag-search-move-prev-line ()
  "Move to previous title."
  (interactive)
  (when (< 3 (line-number-at-pos))
    (call-interactively 'previous-line)))

(defun ag-search-move-next-line ()
  "Move to next title."
  (interactive)
  (when (< (line-number-at-pos)
           (- (line-number-at-pos (point-max)) 1))
    (call-interactively 'next-line)))

(defun ag-search-exit-window ()
  "kill ag-search buffer."
  (interactive)
  (let ((buf (current-buffer)))
    (set-window-configuration ag-search-return-window-config)
    (kill-buffer buf)))

(defun ag-search-quit-window ()
  "Quit ag-search buffer."
  (interactive)
  (set-window-configuration ag-search-return-window-config))

(provide 'ams-glossary)
;;; ams-glossary.el ends here
