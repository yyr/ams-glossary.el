;;; ams-glossary.el -- Read AMS glossary from Emacs

;; Copyright (C) 2012 Yagnesh Raghava Yakkala <http://yagnesh.org>

;; Author: Yagnesh Raghava Yakkala <yagnesh@live.com>
;; Package-Requires: ((epc "0.1.0"))
;; Version: 0.1dev
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

(require 'epc)

(defgroup ams-glossary nil
  "Client to accessing AMS Glossary site."
  :tag "ams-glossary"
  :group 'external)

(defcustom ag-site nil
  "The AMS Glossary site."
  :group 'ams-glossary)

(defconst ams-glossary-version "0.1dev")

(defvar ag-dir (file-name-directory
                        (or load-file-name buffer-file-name)))

(defcustom ag-cache-dir "~/.ams-glossary/"
  "Directory to store the cache."
  :group 'ams-glossary
  :type 'string)

(provide 'ams-glossary)
;;; ams-glossary.el ends here
