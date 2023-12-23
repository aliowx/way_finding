### JWT authentication flow

```mermaid
sequenceDiagram
    client->>+auth: login whit username and password
    auth-->>-client: get JWT tokens
    auth-->>+client: verify user
    client->>endpoints: call services
    client->>auth: access token expire, send refresh token
    auth-->>+client: new access token
    client->>endpoints: call services
```
