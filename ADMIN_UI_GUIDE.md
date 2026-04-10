# Admin Locker Management - UI Guide

## ✅ Now Fully Functional!

As an admin, you can now **Create**, **Edit**, and **Delete** lockers directly from the UI!

---

## How to Use Admin Features

### 1. Login as Admin
- **URL**: http://localhost:8000
- **Username**: admin
- **Password**: admin123

You'll see the **"Admin Panel"** tab appear in the navigation.

---

### 2. Create a New Locker

1. Click **"Admin Panel"** tab
2. Fill in the form:
   - **Locker Number**: e.g., "A101"
   - **Location**: e.g., "Building A - Floor 1"
   - **Size**: Select from dropdown (Small/Medium/Large)
3. Click **"Create Locker"** button
4. Success! Locker is created and appears in "All Lockers"

---

### 3. Edit a Locker

1. Click **"All Lockers"** tab
2. Find the locker you want to edit
3. Click the **"Edit"** button (blue button)
4. A modal dialog opens with the locker details
5. Update any fields:
   - Locker Number
   - Location
   - Size
   - Status (Available/Occupied/Maintenance/Deactivated)
6. Click **"Update Locker"** button
7. Success! Changes are saved

**Example Use Cases:**
- Change status to "Maintenance" when locker needs repair
- Update location if locker is moved
- Change size classification
- Fix typos in locker number

---

### 4. Delete (Deactivate) a Locker

1. Click **"All Lockers"** tab
2. Find the locker you want to remove
3. Click the **"Delete"** button (red button)
4. Confirm the deletion in the popup
5. Success! Locker is deactivated

**Note:** This is a **soft delete** - the locker status is set to "deactivated" instead of being permanently removed from the database. This preserves reservation history.

---

## Visual Guide

### Admin View - Locker Card
```
┌─────────────────────────────┐
│ Locker #A101                │
│ 📍 Building A - Floor 1     │
│ 📏 Size: medium             │
│                             │
│ [AVAILABLE] (green badge)   │
│                             │
│ ┌──────────┬──────────┐     │
│ │   Edit   │  Delete  │     │
│ │  (Blue)  │  (Red)   │     │
│ └──────────┴──────────┘     │
└─────────────────────────────┘
```

### Regular User View - Locker Card
```
┌─────────────────────────────┐
│ Locker #A101                │
│ 📍 Building A - Floor 1     │
│ 📏 Size: medium             │
│                             │
│ [AVAILABLE] (green badge)   │
│                             │
│ ┌────────────────────────┐  │
│ │     Reserve (Green)    │  │
│ └────────────────────────┘  │
└─────────────────────────────┘
```

---

## Edit Modal Dialog

When you click "Edit", a popup appears:

```
┌──────────────────────────────────┐
│       ✏️ Edit Locker             │
├──────────────────────────────────┤
│                                  │
│ Locker Number: [A101        ]    │
│                                  │
│ Location:      [Building A  ]    │
│                                  │
│ Size:          [▼ Medium    ]    │
│                                  │
│ Status:        [▼ Available ]    │
│                                  │
│ ┌──────────────┬───────────────┐ │
│ │Update Locker │    Cancel     │ │
│ │   (Green)    │   (Gray)      │ │
│ └──────────────┴───────────────┘ │
└──────────────────────────────────┘
```

---

## Admin Panel Features Summary

| Feature | Location | How to Access |
|---------|----------|---------------|
| **Create Locker** | Admin Panel tab | Fill form and submit |
| **Edit Locker** | All Lockers tab | Click "Edit" button on any locker |
| **Delete Locker** | All Lockers tab | Click "Delete" button on any locker |
| **View All Lockers** | All Lockers tab | Automatic on tab click |
| **View Available** | Available Lockers tab | Automatic on tab click |

---

## Status Management

### When to Use Each Status:

- **Available**: Locker is ready to be reserved
- **Occupied**: Locker is currently in use (set automatically when reserved)
- **Maintenance**: Locker needs repair or cleaning
- **Deactivated**: Locker is permanently removed from service

### Admin Can Change Status To:
- ✅ Available (make it bookable again)
- ✅ Occupied (manually occupy if needed)
- ✅ Maintenance (temporarily disable for repairs)
- ✅ Deactivated (permanently remove)

---

## Cache Behavior

### When Cache is Invalidated:
1. ✅ Admin creates a locker
2. ✅ Admin edits a locker's status
3. ✅ Admin deletes/deactivates a locker
4. ✅ User reserves a locker
5. ✅ User releases a locker

### What This Means:
- After you edit/delete a locker, the "Available Lockers" list updates automatically
- Changes are reflected immediately in the UI
- Cache ensures fast loading for users

---

## Testing the Features

### Test 1: Create Locker
1. Login as admin
2. Go to "Admin Panel"
3. Create locker: B202, Building B, Large
4. Go to "All Lockers" - see the new locker

### Test 2: Edit Locker
1. Go to "All Lockers"
2. Find locker A101
3. Click "Edit"
4. Change status to "Maintenance"
5. Click "Update Locker"
6. See the locker now shows orange border (maintenance)

### Test 3: Delete Locker
1. Go to "All Lockers"
2. Find a test locker
3. Click "Delete"
4. Confirm deletion
5. Locker now shows gray border (deactivated)

### Test 4: Verify Cache
1. Go to "Available Lockers"
2. Edit a locker, change status to "Maintenance"
3. Go back to "Available Lockers"
4. Locker no longer appears (correct!)

---

## Troubleshooting

### Edit Button Not Showing?
- Make sure you're logged in as **admin** (check the badge)
- Refresh the page
- Check browser console for errors (F12)

### Delete Not Working?
- Confirm you're admin
- Check if you're logged in (token might have expired)
- Try logging out and back in

### Changes Not Reflecting?
- Click "Refresh" button
- Switch tabs and come back
- Check browser console for errors

---

## API Endpoints Used

The UI uses these endpoints behind the scenes:

### Create Locker
```
POST /api/lockers/
Body: { locker_number, location, size, status }
```

### Update Locker
```
PUT /api/lockers/<id>/
Body: { locker_number, location, size, status }
```

### Delete Locker
```
DELETE /api/lockers/<id>/
```

All require admin authentication via JWT token.

---

## What's New

### Before:
- ❌ Could only create lockers
- ❌ No way to edit lockers in UI
- ❌ No way to delete lockers in UI
- ❌ Had to use API directly

### Now:
- ✅ Create lockers via UI
- ✅ Edit lockers with modal dialog
- ✅ Delete (deactivate) lockers with one click
- ✅ All changes reflected immediately
- ✅ Cache automatically invalidated
- ✅ Beautiful, intuitive interface

---

## Summary

**As admin, you now have full control:**

1. **Create** → Admin Panel tab
2. **Read** → All Lockers / Available Lockers tabs
3. **Update** → Edit button on each locker
4. **Delete** → Delete button on each locker

**Full CRUD operations available in the UI!** 🎉

---

**Need Help?**
- Check browser console (F12) for errors
- Verify you're logged in as admin
- Ensure server is running: `python manage.py runserver`
