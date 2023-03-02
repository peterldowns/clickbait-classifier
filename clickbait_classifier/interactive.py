#!/usr/bin/env python
# coding: utf-8

import signal
import sys

def main():
  signal.signal(signal.SIGINT, lambda signal, frame: sys.exit(0))

  print("Loading classifier (may take time to train.)")
  from . import classifier  # noqa: E402
  print("Done.")

  while True:
      try:
          title = input("\nArticle title: ").strip()
      except EOFError:
          break
      if title in ["quit", "exit", "cancel"]:
          break
      probabilities = classifier.classify(title)
      print(
          (
              "({0:.2f}% clickbait, {1:.2f}% news) -> {2}".format(
                  probabilities["clickbait"] * 100,
                  probabilities["news"] * 100,
                  "news" if probabilities["news"] >= 0.5 else "clickbait",
              )
          )
      )
if __name__ == '__main__':
    main()
