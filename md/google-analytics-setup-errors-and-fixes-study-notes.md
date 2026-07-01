# Google Analytics Setup Study Notes — eMarkaz Course Library

## Project

**Project name:** eMarkaz Course Library  
**Website:** `https://emarkazlibrary.com`  
**Google Analytics property:** `eMarkaz Course Library`  
**Measurement ID:** `G-EYX0RYKW7N`

---

## 1. Goal

The goal was to add Google Analytics to the eMarkaz Course Library website so we can see reports such as:

```text
How many people visit the website
Which pages they open
Which courses and semesters are popular
Which country visitors come from
Which device/browser visitors use
How many people are active right now
File downloads
Scrolls
Outbound clicks
```

---

## 2. Important Privacy Point

Google Analytics can show visitor statistics, but it does **not** show exact personal identity.

It can show:

```text
Country
City
Device
Browser
Page views
Traffic source
Active users
```

It cannot normally show:

```text
Exact visitor name
Exact personal identity
```

unless the website has login, signup, or form tracking.

---

## 3. Create Google Analytics Property

Go to:

```text
https://analytics.google.com
```

Create a new property.

Recommended property name:

```text
eMarkaz Course Library
```

Recommended reporting time zone:

```text
United States → Chicago / Central Time
```

Currency:

```text
US Dollar ($)
```

---

## 4. Business Details

For the business details screen:

### Industry category

Recommended:

```text
Education
```

If available, choose:

```text
Online Education
Education & Training
Reference / Education
```

### Business size

Recommended:

```text
Small - 1 to 10 employees
```

This is suitable for a personal or small educational website.

---

## 5. Business Objectives

Recommended objectives:

```text
Understand web and/or app traffic
View user engagement & retention
```

These are best for a library website because we want to know:

```text
How many visitors came
Which pages they explored
Which courses and semesters they used
How long they stayed
```

---

## 6. Data Stream Setup

Choose platform:

```text
Web
```

Because eMarkaz Library is a website, not an Android or iOS app.

Use:

```text
Website URL: https://emarkazlibrary.com
Stream name: eMarkaz Course Library
```

Then click:

```text
Create & continue
```

---

## 7. Enhanced Measurement

Keep **Enhanced measurement ON**.

Important options to keep ON:

```text
Page views
Scrolls
Outbound clicks
File downloads
```

For eMarkaz Course Library, **File downloads** is especially important because visitors may download PDF, DOCX, or XLSX files.

Other options can also remain ON:

```text
Site search
Form interactions
Video engagement
```

---

## 8. Measurement ID

Google Analytics created this Measurement ID:

```text
G-EYX0RYKW7N
```

This ID must be added to the website code.

---

## 9. Google Analytics Code

The Google Analytics code should be placed inside the `<head>` section of `index.html`, before:

```html
</head>
```

Final code:

```html
<!-- Google tag (gtag.js) - Google Analytics Measurement ID: G-EYX0RYKW7N -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-EYX0RYKW7N"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-EYX0RYKW7N');
</script>
```

---

## 10. File Updated

The main homepage file was updated:

```text
/c/Linux/emarkaz-course-library/index.html
```

The Google Analytics script was added inside:

```html
<head>
  ...
</head>
```

---

## 11. Push Changes to GitHub

After editing `index.html`, push the changes:

```bash
cd /c/Linux/emarkaz-course-library

git status

git add -A

git commit -m "Add Google Analytics tracking ID"

git push origin main
```

Then wait for GitHub Pages to redeploy.

---

## 12. Test the Website

Open the live website:

```text
https://emarkazlibrary.com
```

Visit some pages:

```text
Homepage
Courses section
Semester pages
PDF pages
Download buttons
```

---

## 13. Test in Google Analytics

In Google Analytics, go to:

```text
Reports → Realtime
```

Or click:

```text
Test installation
```

Realtime report should show:

```text
Active users in last 30 minutes
Country
Pages being viewed
Events
```

---

## 14. Successful Result

Google Analytics showed:

```text
Active users in last 30 minutes: 2
Country: United States
Measurement ID: G-EYX0RYKW7N
```

This confirmed that Google Analytics was working.

---

# Errors and Fixes

## Error 1: No data received from your website yet

### Message

```text
No data received from your website yet
```

### Cause

This can appear when:

```text
The tag was just installed
GitHub Pages has not redeployed yet
No visitor has opened the live website yet
Analytics dashboard has not refreshed yet
```

### Fix

Open the website:

```text
https://emarkazlibrary.com
```

Then go to:

```text
Reports → Realtime
```

Wait a few minutes.

If Realtime shows active users, the tag is working even if the top message still says no data received.

---

## Error 2: Measurement ID placeholder still present

### Problem

The HTML file had placeholder text:

```text
G-XXXXXXXXXX
```

### Cause

Google Analytics code was added before the real Measurement ID was created.

### Fix

Replace both occurrences of:

```text
G-XXXXXXXXXX
```

with:

```text
G-EYX0RYKW7N
```

Correct lines:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-EYX0RYKW7N"></script>
```

and:

```html
gtag('config', 'G-EYX0RYKW7N');
```

---

## Error 3: Confusing comment in HTML

### Problem

The code had a comment saying:

```html
<!-- Replace G-EYX0RYKW7N with your real Google Analytics Measurement ID -->
```

### Cause

The comment was from the earlier placeholder version and was no longer correct.

### Fix

Replace it with a clean comment:

```html
<!-- Google tag (gtag.js) - Google Analytics Measurement ID: G-EYX0RYKW7N -->
```

or remove the comment completely.

---

## Error 4: Analytics setup screen asked for business details

### Problem

Google Analytics asked:

```text
Industry category
Business size
Business objectives
```

### Fix

Use these values:

```text
Industry category: Education
Business size: Small - 1 to 10 employees
Objectives:
- Understand web and/or app traffic
- View user engagement & retention
```

---

## Error 5: Which platform to choose?

### Problem

Google Analytics asked:

```text
Web
Android app
iOS app
```

### Fix

Choose:

```text
Web
```

Because the project is a static website hosted on GitHub Pages.

---

## Error 6: Which URL to enter?

### Problem

Google Analytics asked for website URL.

### Fix

Use:

```text
https://emarkazlibrary.com
```

Make sure the dropdown is set to:

```text
https://
```

not:

```text
http://
```

Stream name:

```text
eMarkaz Course Library
```

---

## Error 7: Realtime shows users, but Home still says no data

### Problem

Home screen showed:

```text
No data received from your website yet
```

but Realtime showed:

```text
Active users in last 30 minutes: 2
```

### Explanation

Realtime data updates quickly. The main Home dashboard message may take longer to refresh.

### Fix

No action needed if Realtime shows users.

Wait:

```text
24–48 hours
```

for normal reports.

---

## 15. Reports to Use

### Realtime Report

Path:

```text
Reports → Realtime
```

Shows:

```text
Users in last 30 minutes
Country
Pages currently viewed
Events
```

### Pages and Screens

Path:

```text
Reports → Engagement → Pages and screens
```

Shows:

```text
Most visited pages
Course pages
Semester pages
Popular pages
```

### Traffic Acquisition

Path:

```text
Reports → Acquisition → Traffic acquisition
```

Shows:

```text
Direct visitors
Google Search
Social media
Referral websites
```

### Tech Details

Path:

```text
Reports → Tech → Tech details
```

Shows:

```text
Device category
Browser
Operating system
Screen resolution
```

### Demographic Details

Path:

```text
Reports → User attributes → Demographic details
```

Shows:

```text
Country
City
Region
Language
```

---

## 16. Important Waiting Time

Realtime reports can show quickly.

Normal reports can take:

```text
24–48 hours
```

So after first setup, check Realtime immediately, then check normal reports the next day.

---

## 17. Final Working Setup

Final Measurement ID:

```text
G-EYX0RYKW7N
```

Final website:

```text
https://emarkazlibrary.com
```

Final Analytics property:

```text
eMarkaz Course Library
```

Final code location:

```text
index.html → inside <head>
```

---

## 18. Final Workflow for Future Updates

Whenever `index.html` is updated:

```bash
cd /c/Linux/emarkaz-course-library

git status

git add -A

git commit -m "Update homepage"

git push origin main
```

Then test:

```text
https://emarkazlibrary.com
```

And check Analytics:

```text
Reports → Realtime
```

---

## 19. Summary

Google Analytics setup required:

```text
Create property
Create web data stream
Get Measurement ID
Add Google tag to index.html
Push to GitHub
Open website
Check Realtime report
```

Main fixes:

```text
Replace placeholder Measurement ID
Clean wrong comment
Push final index.html
Wait for Google Analytics to receive data
Use Realtime report for quick testing
```

Final result:

```text
Google Analytics successfully started tracking eMarkaz Course Library.
