# Ejendomsskat dokumenter

## Intro

The robot uses OCR to read the case number from pdf documents in a given folder
and renames the documents to the case number. Appending a (index) to duplicates.

OCR is needed because the pdf document consists of a flat image instead of readable text.

## Prerequisites

The robot needs Tesseract OCR to be on the path.

## Process arguments

The robot expects the full path to the document folder as the sole process argument.
