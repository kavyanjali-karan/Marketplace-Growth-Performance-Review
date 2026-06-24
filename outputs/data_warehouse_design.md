# Enterprise Data Warehouse Design

## Marketplace Revenue Recovery & Customer Retention Intelligence System

### Purpose

This document defines the analytical data warehouse architecture used to support executive reporting, customer retention analysis, revenue monitoring, operational performance tracking, and business reviews.

The objective is to create a single source of truth for all marketplace reporting.

---

# Data Warehouse Objectives

The warehouse must support:

Executive Reporting

Customer Analytics

Retention Analytics

Revenue Analytics

Category Analytics

Operational Analytics

Business Reviews

Root Cause Analysis

Forecasting

Strategic Planning

---

# Star Schema Architecture

The warehouse follows a dimensional modeling approach.

Benefits:

Consistent KPI calculation

Faster reporting

Scalable analytics

Executive dashboard support

Metric governance

Simplified business consumption

---

# Fact Table

## Fact Orders

### Grain

One row per completed order.

### Primary Key

Order ID

### Business Purpose

Core revenue and transaction reporting.

### Measures

Order Revenue

Order Value

Payment Value

Freight Value

Review Score

Delivery Days

Purchase Timestamp

Delivery Timestamp

Estimated Delivery Timestamp

---

### Consumed By

Executive Dashboard

Revenue Reporting

Retention Analysis

Operational Analytics

Quarterly Business Reviews

---

# Fact Customer Activity

### Grain

One row per customer per order.

### Primary Key

Customer ID + Order ID

### Business Purpose

Customer lifecycle measurement.

### Measures

Order Count

Revenue Generated

Average Order Value

Days Between Purchases

Customer Lifetime Revenue

---

### Consumed By

Retention Reporting

Segmentation Reporting

Customer Analytics

Executive Reviews

---

# Fact Product Sales

### Grain

One row per product per order.

### Primary Key

Order ID + Product ID

### Business Purpose

Product and category performance tracking.

### Measures

Sales Revenue

Units Sold

Freight Cost

Average Selling Price

---

### Consumed By

Category Dashboards

Revenue Reporting

Category Reviews

Strategic Planning

---

# Fact Delivery Performance

### Grain

One row per order.

### Primary Key

Order ID

### Business Purpose

Operational performance measurement.

### Measures

Delivery Days

Late Delivery Flag

SLA Compliance Flag

Order Status

---

### Consumed By

Operations Dashboard

Customer Experience Reporting

Executive Reviews

---

# Dimension Tables

## Dim Customer

### Primary Key

Customer ID

### Attributes

Customer Unique ID

City

State

First Purchase Date

Latest Purchase Date

Customer Segment

Lifetime Revenue Tier

Retention Status

---

### Business Purpose

Customer segmentation and retention analysis.

---

## Dim Product

### Primary Key

Product ID

### Attributes

Product Category

Category Name

Product Weight

Product Dimensions

Product Revenue Tier

---

### Business Purpose

Category and product performance analysis.

---

## Dim Seller

### Primary Key

Seller ID

### Attributes

Seller City

Seller State

Seller Performance Tier

Seller Revenue Tier

---

### Business Purpose

Marketplace supply-side reporting.

---

## Dim Date

### Primary Key

Date Key

### Attributes

Date

Day

Week

Month

Quarter

Year

Fiscal Quarter

Fiscal Year

---

### Business Purpose

Standardized time intelligence.

---

## Dim Geography

### Primary Key

Geography Key

### Attributes

State

City

Region

Country

---

### Business Purpose

Regional performance reporting.

---

# Relationship Design

Fact Orders

Links To

Dim Customer

Dim Date

Dim Geography

---

Fact Product Sales

Links To

Dim Product

Dim Seller

Dim Date

---

Fact Customer Activity

Links To

Dim Customer

Dim Date

---

Fact Delivery Performance

Links To

Dim Customer

Dim Geography

Dim Date

---

# Executive KPI Source Tables

Gross Merchandise Value

Source

Fact Orders

---

Revenue Growth

Source

Fact Orders

---

Customer Lifetime Value

Source

Fact Customer Activity

---

Repeat Purchase Rate

Source

Fact Customer Activity

---

Revenue Retention Rate

Source

Fact Customer Activity

---

Category Revenue

Source

Fact Product Sales

---

Delivery SLA Compliance

Source

Fact Delivery Performance

---

# Slowly Changing Dimensions

Customer Segment

Type 2

Reason

Customer value changes over time.

---

Customer Retention Status

Type 2

Reason

Customer lifecycle changes.

---

Seller Performance Tier

Type 2

Reason

Seller performance evolves.

---

# Data Refresh Strategy

Orders

Daily

---

Customers

Daily

---

Products

Daily

---

Sellers

Daily

---

Executive Reporting Layer

Daily

---

# Data Quality Controls

Referential Integrity Validation

Duplicate Detection

Null Validation

Revenue Reconciliation

Freshness Monitoring

Metric Certification

---

# Business Intelligence Engineering Ownership

BI Engineering owns:

Data Modeling

Warehouse Governance

Metric Layer

Dashboard Layer

Data Quality Controls

Executive Reporting Infrastructure

---

# Executive Outcome

The warehouse establishes a governed analytical foundation supporting executive reporting, customer analytics, operational monitoring, retention analysis, and strategic decision-making across the marketplace organization.
