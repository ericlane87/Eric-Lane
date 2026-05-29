(function () {
  var path = window.location.pathname.toLowerCase();
  var file = path.substring(path.lastIndexOf("/") + 1);

  if (file === "analytics.html") {
    return;
  }

  var config = window.PORTFOLIO_ANALYTICS || {};

  if (
    config.provider === "cloudflare" &&
    config.cloudflareToken &&
    config.cloudflareToken !== "REPLACE_WITH_CLOUDFLARE_WEB_ANALYTICS_TOKEN"
  ) {
    var script = document.createElement("script");
    script.defer = true;
    script.src = "https://static.cloudflareinsights.com/beacon.min.js";
    script.setAttribute(
      "data-cf-beacon",
      JSON.stringify({ token: config.cloudflareToken })
    );
    document.head.appendChild(script);
  }
})();
