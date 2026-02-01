# Technical Analysis Table Formatting Guidelines

## Quick Reference Table Format

When presenting multiple stock analyses, use properly aligned markdown tables.

### ✅ CORRECT Format (properly aligned):

```markdown
| Ticker | Price   | Change      | Daily Trend       | Weekly Trend      | Verdict             |
|--------|---------|-------------|-------------------|-------------------|---------------------|
| META   | $716.50 | -2.95%      | ✅ Above all MAs  | ✅ Above all MAs  | ✅✅ Strong Bull     |
| BABA   | $169.56 | -2.69%      | ✅ Above all MAs  | ✅ Above all MAs  | ✅✅ Strong Bull     |
| AAOI   | $43.61  | **+10.21%** | ✅ Above all MAs  | ✅ Above all MAs  | ✅✅ Momentum Beast  |
| FLR    | $46.19  | -1.64%      | ✅ Above all MAs  | ✅ Above all MAs  | ✅✅ Strong Bull     |
```

### ❌ INCORRECT Format (misaligned):

```markdown
| Ticker | Price   | Change  | Daily Trend     | Weekly Trend    | Verdict           |
| ------ | ------- | ------- | --------------- | --------------- | ----------------- |
| **META**   | $716.50 | -2.95%  | ✅ Above all MAs | ✅ Above all MAs | ✅✅ Strong Bull    |
```

## Options Flow Table Format

When presenting options flow data, use the same alignment principles:

### ✅ CORRECT Format:

```markdown
| Date        | Type         | Strike | Expiry     | DTE | Contracts | Sentiment |
|-------------|--------------|--------|------------|-----|-----------|-----------|
| 01-29 11:41 | Puts Sold    | 690P   | 03-06      | 34  | 1,550     | Bullish   |
| 01-29 09:59 | Puts Sold    | 550P   | 01-21-28   | 721 | 1,000     | Bullish   |
| 01-29 09:58 | Calls Bought | 1100C  | 01-21-28   | 721 | 1,000     | Bullish   |
| 01-29 09:41 | Puts Sold    | 635P   | 03-20      | 48  | 1,800     | Bullish   |
| 01-28 11:38 | Calls Bought | 700C   | 01-30      | exp | 2,000     | Bullish   |
| 01-28 09:56 | Puts Sold    | 610P   | 05-15      | 104 | 2,400     | Bullish   |
| 01-28 09:53 | Calls Bought | 690C   | 02-04      | 4   | 2,000     | Bullish   |
```

### ❌ INCORRECT Format:

```markdown
| Date        | Type         | Strike | Expiry   | DTE     | Contracts | Sentiment |
| ----------- | ------------ | ------ | -------- | ------- | --------- | --------- |
| 01-29 11:41 | **Puts Sold**    | 690P   | 03-06    | 34      | 1,550     | Bullish   |
```

## Key Rules

1. **No extra spaces in cells**: Each cell should have content followed immediately by the pipe `|`, with only one space on each side
2. **Consistent column widths**: Align columns by adjusting the separator row dashes
3. **No markdown formatting in data cells**: Don't use `**Text**` for bold - use plain text only (applies to ALL columns: ticker, type, sentiment, etc.)
4. **Uniform spacing**: Keep spacing consistent across all rows
5. **No trailing spaces**: Remove any spaces after cell content and before the closing `|`

## Implementation

When formatting multi-ticker analysis results:

```
| Ticker | Price   | Change      | Daily Trend       | Weekly Trend      | Verdict             |
|--------|---------|-------------|-------------------|-------------------|---------------------|
```

- Ticker: 6-8 chars wide, plain text
- Price: 7-9 chars, includes dollar sign
- Change: 11-13 chars, includes percent sign and sign (+/-)
- Daily Trend: 17-19 chars
- Weekly Trend: 17-19 chars
- Verdict: 19-21 chars
