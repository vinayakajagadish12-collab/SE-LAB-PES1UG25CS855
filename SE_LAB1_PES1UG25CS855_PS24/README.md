# Public Bus Live Tracking & Crowding Estimator

## Overview

The **Public Bus Live Tracking & Crowding Estimator** is a municipal
transit intelligence platform designed to help commuters track buses in
real time and understand current crowding levels.

The system ingests GPS coordinates from city buses, calculates estimated
arrival times (ETA) for upcoming stops, and estimates passenger crowding
levels using ticketing sensor data.

## Problem Statement

**Problem Statement #24 --- Smart Cities, Transport & Logistics**

The platform focuses on improving public transportation visibility by
providing:

-   Live bus location tracking
-   Continuously updated arrival-time estimates
-   Passenger crowding estimates
-   Delay notifications for commuters
-   Fleet monitoring for fleet controllers
-   Configurable route-specific delay-alert thresholds

## Actors

### 1. Commuter

The commuter can:

-   View the live location of a selected bus.
-   View the ETA for a selected bus and stop.
-   View the estimated crowding level.
-   Receive an in-app notification when the ETA increases by more than 5
    minutes.

### 2. Fleet Controller

The fleet controller can:

-   Monitor the status of the active fleet.
-   View the current route, latest GPS timestamp, and crowding level of
    active vehicles.
-   Configure delay-alert thresholds for individual routes.
-   Authenticate before accessing controller functions.

## Functional Requirements

  -----------------------------------------------------------------------
  ID                      Priority                Requirement
  ----------------------- ----------------------- -----------------------
  FR-001                  High                    Ingest bus GPS
                                                  coordinates every 5
                                                  seconds and recalculate
                                                  arrival ETAs for
                                                  upcoming route stops.

  FR-002                  High                    Estimate passenger
                                                  crowding as Low,
                                                  Medium, or High using
                                                  ticketing sensor counts
                                                  and refresh the
                                                  estimate when a
                                                  ticketing event is
                                                  received.

  FR-003                  High                    Allow commuters to view
                                                  the live location of a
                                                  selected bus on a map,
                                                  updated at least every
                                                  5 seconds while the bus
                                                  is en route.

  FR-004                  Medium                  Notify commuters in-app
                                                  when the ETA of a
                                                  tracked bus increases
                                                  by more than 5 minutes
                                                  from the previously
                                                  displayed ETA.

  FR-005                  Medium                  Provide the Fleet
                                                  Controller with a
                                                  dashboard of active
                                                  vehicles and allow
                                                  route-specific
                                                  delay-alert thresholds
                                                  to be configured.
  -----------------------------------------------------------------------

## Non-Functional Requirements

### Performance & Security

The tracking engine should support telemetry streams from up to **1,000
active transit vehicles** simultaneously over authenticated and
encrypted channels.

The target is to recalculate ETA within **2 seconds of telemetry
ingestion** under the simulated peak load.

### Reliability & Availability

The commuter-facing tracking and ETA services should provide **99.5%
monthly availability**.

When vehicle telemetry is delayed or lost, the system should degrade
gracefully by showing the last-known position/ETA together with a
**"data delayed"** indicator instead of failing silently.

## Use-Case Diagram

The UML use-case diagram contains two actors: **Commuter** and **Fleet
Controller**.

![Public Bus Live Tracking & Crowding Estimator Use-Case
Diagram](UseCase_Diagram.png)

### Main Use Cases

-   **View Live Bus Location**
-   **View ETA**
-   **Calculate ETA from GPS Feed**
-   **Notify Commuter of Delay (\>5 min)**
-   **View Crowding Estimate**
-   **Estimate Crowding Level from Sensors**
-   **Monitor Fleet Status**
-   **Configure Route Alert Thresholds**
-   **Authenticate User**

### UML Relationships

The diagram uses the following relationships:

-   `View ETA` **includes** `Calculate ETA from GPS Feed`.
-   `View Crowding Estimate` **includes**
    `Estimate Crowding Level from Sensors`.
-   `Configure Route Alert Thresholds` **includes** `Authenticate User`.
-   `Notify Commuter of Delay` **extends** `View ETA` when
    `{ETA delay > threshold}`.

## View ETA --- Use-Case Flow

### Primary Actor

**Commuter**

### Preconditions

1.  The commuter has the app open and has selected a bus/route to track.
2.  The selected bus is actively transmitting GPS telemetry.
3.  The commuter's device has network connectivity.

### Main Success Scenario

1.  The commuter selects a bus/route and a target stop.
2.  The system retrieves the latest GPS coordinate for the selected bus.
3.  The system calculates the ETA using the bus's current position,
    distance to the stop, and current traffic/speed data.
4.  The system displays the ETA and last-updated timestamp.
5.  The system schedules the next ETA refresh according to the 5-second
    GPS ingest cycle.
6.  The ETA continues to refresh automatically while the screen remains
    open.
7.  If the ETA increases by more than 5 minutes, the delay-notification
    use case is triggered.

### Alternate Flow --- GPS Signal Lost / Stale Telemetry

If a fresh GPS update is not received within the expected 5-second
window:

1.  The system marks the telemetry as stale.
2.  The last-known ETA is displayed with a **"data delayed"** indicator.
3.  The system continues attempting to receive the next GPS update.
4.  Once fresh telemetry arrives, ETA calculation resumes.
5.  If telemetry remains stale for more than 2 minutes, the commuter is
    informed that live tracking for the bus is temporarily unavailable.

## Expected Benefits

-   Helps commuters make better travel decisions using live bus
    information.
-   Provides visibility into current bus locations and arrival times.
-   Helps commuters choose less-congested services.
-   Allows fleet controllers to identify stalled vehicles, sensor
    issues, and route delays.
-   Supports route-specific delay-alert configuration.

## Project Information

**Course:** Software Engineering Lab\
**Lab:** Lab 1 --- Requirements Engineering & UML Use-Case Modelling\
**Problem Statement:** #24 --- Smart Cities, Transport & Logistics\
**Project:** Public Bus Live Tracking & Crowding Estimator
