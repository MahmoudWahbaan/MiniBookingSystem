# Meeting Scheduling System - Business Logic

## User Entity
**Attributes**: Username, First Name, Last Name, Email, Password, Contact Number

**Account Structure**: Each user has both Host and Client modules

## Host Module
- **CREATE**: Create free time slots
- **UPDATE**: Modify non-booked slots
- **DELETE**: Remove non-booked slots

## Client Module
- View all hosts with available slots
- Search specific users
- **Book Slot**: Reserve free slots
- **Unbook Slot**: Cancel booking (must be 48+ hours before meeting)

## Meeting Entity
**Attributes**: Client, Host, Start Time, End Time

**States**: `Scheduled` → `Ongoing` → `Ended`

## Time Slot Entity
**States**: `Free` ↔ `Booked`

**Transitions**:
- **Free → Booked**: Client books slot
- **Booked → Free**: Client cancels OR Host frees (must be 48+ hours before meeting)
- **Within 48 hours**: Slot locked as "Booked"

## Constraints
1. Authentication via email/password
2. All users can be both hosts and clients
3. 48-hour cancellation/freeing window
4. Only free slots can be modified by hosts
