;;; ams-glossary.el -- Read AMS glossary from Emacs

;; Copyright (C) 2012, 2015 Yagnesh Raghava Yakkala <http://yagnesh.org>

;; Author: Yagnesh Raghava Yakkala <yagnesh@live.com>
;; Package-Requires: ((s))
;; Version: 0.1
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

()

(provide 'ams-glossary)
;;; ams-glossary.el ends here
