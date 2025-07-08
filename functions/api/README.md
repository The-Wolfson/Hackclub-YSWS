# Hackclub Events
A Slack app to keep you up to date with Hackclub's YSWS programs and events.

## API
### GET
### `/ysws`
lists all ysws programs
- **Filter:**
  - `all`
  - `active` *(default)*
  - `ended`
  - `draft`

- **Sort:**
  - `category`
  - `alphabetical`
  - `date` *(default)*
  - `status`

#### `/:slack_channel`  
  Get details for a specific YSWS program by its Slack channel.

---

### `/hackathons`
lists all hackathons
- **Filter:**
  - `all`
  - `active` *(default)*
  - `ended`
  - `upcoming`

- **Modality:**
  - `all` *(default)*
  - `online`
  - `in-person`
  - `hybrid`

- **Sort:**
  - `modality`
  - `alphabetical`
  - `date` *(default)*

#### `/:id`  
  Get details for a specific hackathon by ID.
  
---

### `/events`
lists all events
- **Filter:**
  - `all` *(default)*
  - `ended`
  - `upcoming`

- **Type:**
  - `all` *(default)*
  - `ama`
  - `event`

- **Sort:**
  - `alphabetical`
  - `date` *(default)*

#### `/:slug`  
  Get details for a specific hackathon by its slug.