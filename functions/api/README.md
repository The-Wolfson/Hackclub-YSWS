# Hackclub YSWS
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

### `/events`
lists all events
- **Filter:**
  - `all` *(default)*
  - `active`
  - `ended`
  - `upcoming`

- **Type:**
  - `all` *(default)*
  - `online`
  - `in-person`
  - `hybrid`

- **Sort:**
  - `type`
  - `alphabetical`
  - `date` *(default)*

#### `/:id`  
  Get details for a specific event by ID.