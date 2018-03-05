from channels import include

channel_routing = [
    # Include subrouting from an app with predefined path matching.
    include("socialmedia.activities.routing.websocket_routing",
            path=r"^/notifications/$"),
    include("socialmedia.feeds.routing.websocket_routing", path=r"^/feeds/$"),
    include("socialmedia.messenger.routing.websocket_routing",
            path=r"^/")
]
