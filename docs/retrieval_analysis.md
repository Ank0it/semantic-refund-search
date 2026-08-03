# Retrieval Analysis

## Evaluation Summary

- Total Evaluation Queries: 20
- Correct Retrievals: 16
- Accuracy: 80%
- Assignment Target: Passed (>=15/20)

---

## Bad Retrieval Case 1

### Query

What happens if I receive the wrong item?

### Expected Category

Returns

### Retrieved

Refund, Exchange, Refund

### Root Cause

The dataset primarily contains terms such as "incorrect product" and "damaged item" but lacks phrases like "wrong item" and "received different item".

### Planned Improvement

Add synonyms including:
- wrong item
- incorrect item
- received different product

---

## Bad Retrieval Case 2

### Query

The refund hasn't reached my bank yet.

### Expected Category

Payments

### Retrieved

Refund, Refund, Support

### Root Cause

Payment-related terminology is underrepresented.

### Planned Improvement

Expand payment chunks with:

- bank refund
- refund delay
- payment reversal
- card refund
- UPI refund

---

## Bad Retrieval Case 3

### Query

Can I undo my purchase?

### Expected Category

Orders

### Retrieved

Support, Refund, Refund

### Root Cause

The dataset contains "cancel order" but not "undo purchase".

### Planned Improvement

Add alternative wording:

- undo purchase
- reverse order
- cancel purchase

---

## Bad Retrieval Case 4

### Query

Warranty

### Expected Category

Warranty

### Retrieved

Exchange, Returns

### Root Cause

The Warranty category contains limited semantic information.

### Planned Improvement

Expand warranty chunks with:

- manufacturer warranty
- guarantee
- warranty replacement
- warranty claim

---

## Conclusion

The semantic search system achieved an evaluation accuracy of 80% (16/20).

Most failures were caused by missing synonyms rather than retrieval model limitations.

Future improvements include richer chunk wording and additional domain-specific terminology.