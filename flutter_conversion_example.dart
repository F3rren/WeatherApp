// Esempio di come potrebbe apparire la conversione Flutter
import 'package:flutter/material.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:geolocator/geolocator.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class WeatherApp extends StatefulWidget {
  @override
  _WeatherAppState createState() => _WeatherAppState();
}

class _WeatherAppState extends State<WeatherApp> {
  final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin =
      FlutterLocalNotificationsPlugin();
  
  @override
  void initState() {
    super.initState();
    _initializeNotifications();
    _startWeatherMonitoring();
  }

  Future<void> _initializeNotifications() async {
    const AndroidInitializationSettings initializationSettingsAndroid =
        AndroidInitializationSettings('@mipmap/ic_launcher');
    
    const InitializationSettings initializationSettings =
        InitializationSettings(android: initializationSettingsAndroid);
    
    await flutterLocalNotificationsPlugin.initialize(initializationSettings);
  }

  Future<void> _showWeatherAlert(String title, String body) async {
    const AndroidNotificationDetails androidPlatformChannelSpecifics =
        AndroidNotificationDetails(
      'weather_alerts',
      'Weather Alerts',
      channelDescription: 'Notifications for weather conditions',
      importance: Importance.max,
      priority: Priority.high,
      showWhen: false,
    );
    
    const NotificationDetails platformChannelSpecifics =
        NotificationDetails(android: androidPlatformChannelSpecifics);
    
    await flutterLocalNotificationsPlugin.show(
      0,
      title,
      body,
      platformChannelSpecifics,
    );
  }

  Future<void> _startWeatherMonitoring() async {
    // Background service che controlla il meteo ogni X minuti
    Timer.periodic(Duration(minutes: 30), (timer) async {
      try {
        Position position = await Geolocator.getCurrentPosition();
        WeatherData weather = await _fetchWeatherData(position);
        
        if (_shouldAlert(weather)) {
          await _showWeatherAlert(
            'Weather Alert',
            'Temperature: ${weather.temperature}°C'
          );
        }
      } catch (e) {
        print('Error monitoring weather: $e');
      }
    });
  }

  Future<WeatherData> _fetchWeatherData(Position position) async {
    // Stessa API OpenWeatherMap che usi già
    const apiKey = 'YOUR_API_KEY';
    final url = 'https://api.openweathermap.org/data/2.5/weather?lat=${position.latitude}&lon=${position.longitude}&appid=$apiKey&units=metric';
    
    final response = await http.get(Uri.parse(url));
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return WeatherData.fromJson(data);
    }
    throw Exception('Failed to fetch weather data');
  }

  bool _shouldAlert(WeatherData weather) {
    // Stessa logica del tuo WeatherAlertsService
    return weather.temperature > 25.0 || weather.temperature < 5.0;
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MeteoApp Flutter',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        brightness: Brightness.light,
      ),
      darkTheme: ThemeData(
        brightness: Brightness.dark,
      ),
      home: WeatherHomeScreen(),
    );
  }
}

class WeatherData {
  final double temperature;
  final String description;
  final String icon;

  WeatherData({
    required this.temperature,
    required this.description,
    required this.icon,
  });

  factory WeatherData.fromJson(Map<String, dynamic> json) {
    return WeatherData(
      temperature: json['main']['temp'].toDouble(),
      description: json['weather'][0]['description'],
      icon: json['weather'][0]['icon'],
    );
  }
}

class WeatherHomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('MeteoApp'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.wb_sunny,
              size: 100,
              color: Colors.orange,
            ),
            SizedBox(height: 20),
            Text(
              '25°C',
              style: TextStyle(
                fontSize: 48,
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              'Sunny',
              style: TextStyle(fontSize: 18),
            ),
          ],
        ),
      ),
    );
  }
}
