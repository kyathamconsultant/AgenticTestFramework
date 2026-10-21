---
name: application-domain
title: E-Commerce QA Risk-Based Testing Framework
description: Comprehensive risk identification and test case design for e-commerce systems with financial, inventory, fraud, and compliance considerations
category: Domain Knowledge
version: 2.0
updated: 2026-10-21
level: Intermediate to Advanced
---

# E-Commerce QA Risk-Based Testing Framework

**Systematic risk identification and testing strategies for e-commerce applications**

---

## 📋 Table of Contents

1. [Financial Risks](#financial-risks)
2. [Inventory Risks](#inventory-risks)
3. [Fraud Risks](#fraud-risks)
4. [Validation Risks](#validation-risks)
5. [Business Rule Risks](#business-rule-risks)
6. [Checkout & Payment Risks](#checkout--payment-risks)
7. [Concurrency Risks](#concurrency-risks)
8. [Boundary Value Testing](#boundary-value-testing)
9. [Risk Categorization Matrix](#risk-categorization-matrix)

---

## Financial Risks

**Priority:** 🔴 **CRITICAL**  
**Impact:** Direct financial loss, revenue impact, customer trust erosion

### Key Risk Areas

| Risk | Description | Test Case Example |
|------|-------------|-------------------|
| **Negative/Zero Prices** | Product prices applied as negative or zero values in cart | Add item with -$10 price; verify system rejects or applies correctly |
| **Discount Overflow** | Discount exceeds product price (>100%) | Apply 150% discount on $100 item; verify cap at 100% or rejection |
| **Tax Calculation Errors** | Incorrect tax on multi-currency transactions | Purchase in USD, GBP, EUR; verify tax calculated per currency rules |
| **Refund Amount Mismatch** | Refund exceeds original transaction amount | Process refund > purchase price; verify system rejects |
| **Hidden Charges** | Unexpected fees appearing after checkout | Complete checkout, verify no hidden charges in final order |
| **Partial Payment Capture** | Payment captured but order shows incomplete | Process payment, verify full amount captured or fails cleanly |
| **Double Charging** | Customer charged twice for single transaction | Submit form once, verify single charge in payment history |
| **Currency Conversion Errors** | Wrong conversion rates applied | Purchase in multiple currencies; verify correct conversion |

### Test Checklist

- [ ] Test zero price items
- [ ] Test negative price values
- [ ] Test discount > 100%
- [ ] Test multi-currency transactions
- [ ] Test refund > original amount
- [ ] Test large order amounts (edge cases)
- [ ] Test decimal precision (e.g., $0.01)
- [ ] Verify transaction audit trail

---

## Inventory Risks

**Priority:** 🔴 **CRITICAL**  
**Impact:** Overselling, customer dissatisfaction, operational issues

### Key Risk Areas

| Risk | Description | Test Case Example |
|------|-------------|-------------------|
| **Negative Stock** | Inventory becomes negative after order | Order 100 items when only 50 available; verify rejection or backorder |
| **Overselling** | More items sold than available in inventory | Concurrent orders for same limited item; verify only correct qty sold |
| **Concurrent Order Depletion** | Multiple orders simultaneously deplete same stock | 2 users order last 5 items simultaneously; verify stock consistency |
| **Inventory Not Reserved** | Stock not reserved during payment processing | Add to cart, complete payment; verify stock deducted atomically |
| **Cross-Warehouse Sync Delays** | Stock updates not reflected across warehouses | Update stock in Warehouse A; verify Warehouse B reflects within timeout |
| **Bundle Item Mismatch** | Bundle items showing incorrect availability | Bundle requires A+B+C; verify availability only if all in stock |
| **Stock After Cancellation** | Stock not restored when order cancelled | Order item, cancel order; verify stock returned to inventory |
| **Pre-Order Items Shipping** | Pre-order items shipping immediately | Mark item as pre-order, purchase; verify ships only after release date |

### Test Checklist

- [ ] Test inventory goes negative
- [ ] Test concurrent purchases of last item
- [ ] Test stock reservation during checkout
- [ ] Test cross-warehouse synchronization
- [ ] Test bundle availability logic
- [ ] Test inventory restoration on cancellation
- [ ] Test pre-order date enforcement
- [ ] Verify inventory audit trail

---

## Fraud Risks

**Priority:** 🔴 **CRITICAL**  
**Impact:** Financial loss, chargeback liability, regulatory issues

### Key Risk Areas

| Risk | Description | Test Case Example |
|------|-------------|-------------------|
| **Duplicate Submission** | Same order submitted multiple times within seconds | Submit checkout form twice rapidly; verify only 1 order created |
| **Multiple Payment Methods** | Multiple transactions with different payment methods in one session | Use Card A, then Card B in same session; verify fraud detection |
| **Bulk Restricted Items** | Extremely high quantity orders for restricted items | Order 1000 units of age-restricted items; verify velocity check |
| **Price Manipulation** | Price changed before final checkout | Add $100 item (cart shows $100), then price changes to $10; verify final price |
| **Account Takeover** | Rapid location/shipping address changes | Change address in USA, then Brazil, then UK in 5 minutes; verify fraud flag |
| **Velocity Attacks** | Multiple failed payments then success | 10 failed attempts, then successful payment; verify account locked |
| **Coupon Code Stacking** | Same coupon applied multiple times | Apply 20% discount 5 times; verify once or system rejects |
| **Gift Card Fraud** | Invalid or already-used gift cards accepted | Use fake GC number; verify rejection and logging |

### Test Checklist

- [ ] Test duplicate order submission
- [ ] Test multiple payment methods in one session
- [ ] Test bulk restricted item purchases
- [ ] Test price manipulation between add-to-cart and checkout
- [ ] Test rapid address changes (velocity)
- [ ] Test failed payment attempt limits
- [ ] Test coupon code duplication
- [ ] Test gift card validation and fraud logging

---

## Validation Risks

**Priority:** 🟡 **HIGH**  
**Impact:** Data integrity, security vulnerabilities, injection attacks

### Key Risk Areas

| Risk | Description | Test Case Example |
|------|-------------|-------------------|
| **SQL Injection** | SQL injection in search, category, or product filter fields | Search for `'; DROP TABLE products; --`; verify no injection |
| **XSS Vulnerabilities** | XSS in user reviews and product comments | Add comment: `<script>alert('XSS')</script>`; verify sanitized |
| **Non-Numeric Quantity** | Non-numeric characters in quantity fields | Enter qty "abc" or "5@2"; verify validation error |
| **Invalid Email Format** | Email validation bypassed with special characters | Use `test@@example.com` or `test.example.com`; verify rejection |
| **Credit Card Validation** | Credit card number length validation missing | Enter 10-digit card number; verify Luhn algorithm check |
| **Expired Coupon Codes** | Expired coupons still apply discount | Use expired coupon; verify rejection with clear message |
| **Postal Code Format** | Postal code validation missing or incorrect | Enter "ABC" as postal code; verify format validation per country |
| **Phone Number Format** | Phone number accepts invalid formats | Enter "abc" as phone; verify format validation |

### Test Checklist

- [ ] Test SQL injection in all search fields
- [ ] Test XSS in comments/reviews
- [ ] Test non-numeric quantity fields
- [ ] Test email format validation
- [ ] Test credit card Luhn algorithm
- [ ] Test expired coupon rejection
- [ ] Test postal code format per country
- [ ] Test phone number format validation

---

## Business Rule Risks

**Priority:** 🟡 **HIGH**  
**Impact:** Incorrect business logic, revenue leakage

### Key Risk Areas

| Risk | Description | Test Case Example |
|------|-------------|-------------------|
| **Free Shipping Threshold** | Free shipping threshold not enforced correctly | Order $49.99 (threshold $50); verify shipping charged correctly |
| **Loyalty Points Calculation** | Loyalty points not calculated on discounted items | Buy $100 item with 50% discount; verify points on $100 or $50 |
| **Bulk Discount Tiers** | Bulk discounts applying incorrectly | Buy 5 items at tier 1, 10 items at tier 2; verify correct discount |
| **Cart Abandonment Emails** | Cart abandonment emails sent to wrong users | Abandon cart as User A; verify email sent to User A only |
| **Duplicate Items in Cart** | Same product added multiple times not consolidating | Add item twice; verify qty=2 or separate line items (per design) |
| **Applied Coupon on Wrong Items** | Coupon applies to ineligible items | Apply $10 coupon to electronics on "apparel only"; verify rejection |
| **Return Window Enforcement** | Items returnable after return window closes | Order Jan 1, attempt return on Jan 40; verify rejection |
| **Sale Price Effective Dates** | Sale prices not enforced by effective date | Set sale price effective Jan 15; verify regular price before, sale price after |

### Test Checklist

- [ ] Test free shipping threshold logic
- [ ] Test loyalty points on discounted purchases
- [ ] Test multi-tier bulk discounts
- [ ] Test cart abandonment email routing
- [ ] Test duplicate item consolidation
- [ ] Test coupon eligibility rules
- [ ] Test return window enforcement
- [ ] Test sale price effective date logic

---

## Checkout & Payment Risks

**Priority:** 🔴 **CRITICAL**  
**Impact:** Payment failures, compliance violations, data breaches

### Key Risk Areas

| Risk | Description | Test Case Example |
|------|-------------|-------------------|
| **PCI Compliance Violations** | Unencrypted card data stored locally | Verify card data encrypted at rest and in transit |
| **Payment Gateway Timeout** | Payment gateway timeout not handled gracefully | Simulate gateway timeout; verify user-friendly message |
| **Partial Payment Captured** | Partial payment captured but order marked complete | Order $100, only $50 captured; verify order status reflects |
| **CVV Validation Missing** | CVV validation missing or bypassable | Enter invalid CVV; verify rejection before payment attempt |
| **3D Secure Flow** | 3D Secure authentication flow interrupted | Initiate 3DS; cancel during challenge; verify transaction fails |
| **Retry Logic Overcharge** | Retry logic charging customer multiple times | Simulate timeout; verify single charge despite retries |
| **Payment Confirmation Missing** | Confirmation not sent after successful payment | Complete payment; verify confirmation email within timeout |
| **Webhook Failures** | Payment webhooks not processed correctly | Payment success, verify order status updated from webhook |

### Test Checklist

- [ ] Test card data encryption (PCI-DSS)
- [ ] Test payment gateway timeout handling
- [ ] Test partial payment scenarios
- [ ] Test CVV validation
- [ ] Test 3D Secure flow completion
- [ ] Test retry logic prevents double-charge
- [ ] Test confirmation email delivery
- [ ] Test webhook processing for payment updates

---

## Concurrency Risks

**Priority:** 🟡 **HIGH**  
**Impact:** Data corruption, race conditions, inventory inconsistency

### Key Risk Areas

| Risk | Description | Test Case Example |
|------|-------------|-------------------|
| **Simultaneous Checkout** | Two users checkout with last inventory item simultaneously | User A and B both click checkout with last item; verify only 1 succeeds |
| **Race Condition** | Race condition between stock check and order placement | Stock check passes, item sold before order placed; verify handling |
| **Parallel Coupon Application** | Same coupon applied multiple times in parallel | Apply coupon 5 times simultaneously; verify applied once or rejects |
| **Concurrent Wishlist/Cart** | Parallel wishlist and cart modifications | Modify cart and wishlist simultaneously; verify data consistency |
| **Multiple Payment Attempts** | Multiple payment attempts completing simultaneously | Submit payment form twice rapidly; verify single charge |
| **Stock Sync Delay** | Inventory sync delays between order systems | Order placed, stock not immediately reflected; verify eventual consistency |
| **Concurrent User Sessions** | Same user logged in on 2 devices simultaneously | Login device A, then device B; verify single session or handling |
| **Concurrent Admin Changes** | Admin changes price while customer checking out | Raise price mid-checkout; verify clear conflict resolution |

### Test Checklist

- [ ] Test simultaneous last-item purchases
- [ ] Test race conditions in payment processing
- [ ] Test concurrent coupon applications
- [ ] Test cart/wishlist concurrent modifications
- [ ] Test duplicate payment form submissions
- [ ] Test inventory sync under high concurrency
- [ ] Test multi-device session management
- [ ] Test admin/customer concurrent updates

---

## Boundary Value Testing

**Priority:** 🟡 **HIGH**  
**Impact:** Edge case failures, data type errors

### Boundary Value Matrix

| Field | Zero | Minimum Valid | Maximum Valid | Over Maximum | Negative | Decimal |
|-------|------|---------------|---------------|--------------|----------|---------|
| **Price** | Reject | $0.01 | 999999.99 | Reject/Cap | Reject | Accept |
| **Quantity** | Reject | 1 | System Limit | Reject/Cap | Reject | Reject |
| **Discount %** | Accept (0%) | 0.01% | 100% | Reject | Reject | Accept |
| **Tax Rate** | Accept (0%) | 0% | 50% (varies) | Reject | Reject | Accept (e.g., 8.5%) |
| **User ID** | [Verify] | 1 | [Max Int] | [Verify] | Reject | Reject |
| **Product ID** | [Verify] | 1 | [Max Int] | [Verify] | Reject | Reject |

### Test Cases by Boundary

#### **Zero Boundary**
- Order quantity 0 → Should reject
- Price $0.00 → Should reject  
- Discount 0% → Should accept (no discount)
- Tax 0% → Should accept (no tax)

#### **Minimum Valid**
- Order quantity 1 → Should accept
- Price $0.01 → Should accept
- Discount 0.01% → Should accept
- Email length 5 chars → Should accept

#### **Maximum Valid**
- Price $999,999.99 → Should accept
- Quantity 999,999 → Should accept (or system limit)
- Discount 100% → Should accept (full discount)
- Postal code max length → Should accept

#### **Over Maximum**
- Price $1,000,000.00 → Should reject or apply system limit
- Quantity 1,000,000 → Should reject or apply limit
- Discount 150% → Should reject
- Text field > max length → Should truncate or reject

#### **Negative Values**
- Price -$50 → Should reject
- Quantity -5 → Should reject
- Discount -10% → Should reject
- Tax -5% → Should reject

#### **Decimal Precision**
- Price $19.995 → Round correctly ($20.00)
- Tax $15.333... → Round correctly
- Discount 33.333% → Handle precision correctly

---

## Risk Categorization Matrix

### Priority & Severity Mapping

```
PRIORITY MATRIX

High Impact × High Probability = 🔴 CRITICAL (First to fix)
├─ Financial Risks
├─ Payment Processing
├─ Inventory Overselling
└─ Fraud Detection

High Impact × Medium Probability = 🟠 HIGH (Priority fix)
├─ Validation Risks
├─ Business Rule Risks
├─ Concurrency Risks
└─ Data Integrity

Medium Impact × High Probability = 🟡 MEDIUM (Schedule fix)
├─ User Experience Issues
├─ Performance Issues
└─ Non-critical workflows

Low Impact × Low Probability = 🟢 LOW (Backlog)
├─ Minor UI bugs
├─ Non-blocking issues
└─ Enhancement requests
```

### Risk-to-Test-Case Mapping

| Risk Category | # Test Cases | Priority | Frequency |
|---------------|-------------|----------|-----------|
| Financial Risks | 8-10 | 🔴 Critical | Every Sprint |
| Inventory Risks | 8-10 | 🔴 Critical | Every Sprint |
| Fraud Risks | 8-10 | 🔴 Critical | Every Sprint |
| Checkout & Payment | 8-10 | 🔴 Critical | Every Sprint |
| Concurrency Risks | 8-10 | 🟡 High | Weekly |
| Business Rules | 10-15 | 🟡 High | Bi-weekly |
| Validation Risks | 8-12 | 🟡 High | Bi-weekly |
| Boundary Values | 15-20 | 🟡 High | Monthly |

---

## Test Case Structure

### Standard Format

```gherkin
Feature: [Risk Category] - [Feature Name]
  As a [user type]
  I want to [perform action]
  So that [business value]

  Scenario: [Risk scenario title]
    Given [precondition]
    When [action]
    And [additional action]
    Then [expected result - security/correctness]
    And [verification]

  Scenario Outline: [Data-driven risk test]
    When [action with <parameter>]
    Then [expected result with <expected_value>]

    Examples:
      | parameter | expected_value | risk_category |
      | value1    | result1        | Financial     |
      | value2    | result2        | Inventory     |
```

### Example Test Case

```gherkin
Feature: Financial Risk - Discount Overflow Prevention
  As a QA Automation Engineer
  I want to validate discount calculation
  So that customers cannot exceed 100% discount

  @financial @critical @boundary
  Scenario Outline: Discount calculation with boundary values
    Given I add product with price "<price>"
    When I apply discount "<discount_percent>"
    Then the system should "<action>"
    And the discount should be "<expected_discount>"

    Examples:
      | price | discount_percent | action | expected_discount |
      | 100   | 50               | accept | 50.00             |
      | 100   | 99.99            | accept | 99.90             |
      | 100   | 100              | accept | 100.00            |
      | 100   | 100.01           | reject | N/A               |
      | 100   | 150              | reject | N/A               |
```

---

## Implementation Guidelines

### When to Apply Each Risk Category

| Situation | Apply | Reason |
|-----------|-------|--------|
| **Payment Processing Feature** | Financial, Fraud, Concurrency | High-risk transaction area |
| **Cart/Checkout Feature** | Business Rules, Validation, Boundary | Core revenue path |
| **Product Listing** | Inventory, Concurrency, Business Rules | Stock management critical |
| **Discount/Promotion** | Financial, Business Rules, Boundary | Revenue impact, complex logic |
| **User Authentication** | Fraud, Validation, Concurrency | Security-sensitive |
| **Search/Filter** | Validation, Business Rules | Data integrity, injection risks |
| **Reporting/Analytics** | Concurrency, Data Integrity | Consistency critical |
| **Admin Functions** | All categories | Permission elevation risk |

---

## Quick Reference Checklist

### For Each Feature Being Tested

- [ ] Identify all applicable risk categories
- [ ] Document 2-3 test cases per risk
- [ ] Include boundary value tests
- [ ] Add concurrency/race condition tests if applicable
- [ ] Verify no SQL injection vulnerabilities
- [ ] Verify no XSS vulnerabilities
- [ ] Test with invalid/expired data
- [ ] Test with maximum/minimum boundaries
- [ ] Verify audit trails for sensitive operations
- [ ] Test error handling and user messaging
- [ ] Document expected vs actual results
- [ ] Include screenshots/evidence in reports

---

**Version:** 2.0  
**Framework:** Behavior-Driven Development (BDD)  
**Applicable To:** E-Commerce Systems  
**Last Updated:** 2026-10-21  
**Expertise Level:** Intermediate to Advanced
