---
title: How Proof-of-Work Works
description: A closer look at the puzzle miners solve and why it's hard to cheat.
category: Mining
date: 2026-06-08
---

## The core idea

Proof-of-work asks miners to find a number (a "nonce") that, combined with
the block's data and run through a hash function, produces an output below
a target value. There's no shortcut - the only way to find it is to try
huge numbers of guesses.

## Why it's one-way

Hash functions are designed so that:

- The same input always produces the same output
- A tiny change in input produces a completely different output
- You can't work backward from an output to find an input

This means the only practical strategy is brute force - which is exactly
what makes proof-of-work *proof* of real energy and computation spent.

## Difficulty adjustment

Roughly every two weeks, the Bitcoin network adjusts how hard the puzzle is,
based on how quickly the last set of blocks was found. This keeps new blocks
arriving about every ten minutes, even as more or less mining power joins
the network.

*Refresh Labs demonstrates this live in the Living Laboratory - see the
[Living Laboratory](/living-laboratory) page for real operational data.*
