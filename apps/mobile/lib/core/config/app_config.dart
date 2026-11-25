/// Externalized mobile configuration.
///
/// Pass [API_BASE_URL] via `--dart-define`.
/// Examples:
/// - Android emulator → host: `http://10.0.2.2:8080`
/// - Physical Android device → `http://<DEV_MACHINE_LAN_IP>:8080`
/// - Windows desktop: `http://127.0.0.1:8080`
class AppConfig {
  const AppConfig({
    required this.appName,
    required this.apiBaseUrl,
    this.connectTimeout = const Duration(seconds: 5),
    this.receiveTimeout = const Duration(seconds: 10),
  });

  final String appName;
  final String apiBaseUrl;
  final Duration connectTimeout;
  final Duration receiveTimeout;

  factory AppConfig.fromEnvironment() {
    return const AppConfig(
      appName: 'Fitness AI',
      apiBaseUrl: String.fromEnvironment(
        'API_BASE_URL',
        defaultValue: 'http://127.0.0.1:8080',
      ),
    );
  }
}
