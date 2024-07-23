#define HC12 Serial1

enum State : byte
{
  ST_BOOT,
  ST_STANDBY,
  ST_BURN,
  ST_COAST,
  ST_DESCENT,
  ST_LANDED,
  STATE_CNT
};

size_t packet_size[State::STATE_CNT] = {
    1,
    101,
    49,
    45,
    45,
    21};

byte state;
char buffer[200];

void setup()
{
  Serial.begin(115200);
  HC12.begin(9600); 
  delay(2000);
}

void loop()
{
  int bytes = HC12.available();
  if (bytes > 0)
  {
    Serial.print("Bytes available: ");
    Serial.println(bytes);
    state = HC12.read();
    // Serial.println("Received data");
    // Serial.println(state);

    switch (state)
    {
    case State::ST_BOOT:
      read_ST_BOOT();
      break;

    case State::ST_STANDBY:
      read_ST_STANDBY();
      break;

    case State::ST_BURN:
      read_ST_BURN();
      break;

    case State::ST_COAST:
      read_ST_COAST();
      break;

    case State::ST_DESCENT:
      read_ST_DESCENT();
      break;

    case State::ST_LANDED:
      read_ST_LANDED();
      break;

    default:
      Serial.println("Invalid state");
      break;
    }
  }
}

void read_ST_BOOT()
{
  char message[1000];
  sprintf(message, "[%07lu] [STAT] ST_BOOT", millis());
  Serial.println(message);
  return;
}

void read_ST_STANDBY()
{
  HC12.readBytes(buffer, packet_size[State::ST_STANDBY] - 1);
  uint32_t time;
  float gps[8];
  float imu[10];
  float bmp[4];
  float adc[2];

  memcpy(&time, buffer, 4);
  memcpy(gps, buffer + 4, 32);
  memcpy(imu, buffer + 36, 40);
  memcpy(bmp, buffer + 76, 16);
  memcpy(adc, buffer + 92, 8);

  char message[1000];
  sprintf(message, "[%07lu] [STAT] ST_STANDBY\n"
                   "[%07lu] [DATA] [GPS] Lat: %.7f, Lon: %.7f, Alt: %.7f, Geo: %.7f\n"
                   "[%07lu] [DATA] [GPS] Lat_LS: %.7f, Long_LS: %.7f, Alt_LS: %.7f, Geo_LS: %.7f\n"
                   "[%07lu] [DATA] [IMU] Acc: (%.7f, %.7f, %.7f)\n"
                   "[%07lu] [DATA] [IMU] Ang vel: (%.7f, %.7f, %.7f)\n"
                   "[%07lu] [DATA] [IMU] Quat: (%.7f, %.7f, %.7f, %.7f)\n"
                   "[%07lu] [DATA] [BMP] Pres: %.7f, Temp: %.7f\n"
                   "[%07lu] [DATA] [BMP] Pres_LS: %.7f, Temp_LS: %.7f\n"
                   "[%07lu] [DATA] [ADC] V_bat: %.7f, P_chamber: %.7f",
          time,
          time, gps[0], gps[1], gps[2], gps[3],
          time, gps[4], gps[5], gps[6], gps[7],
          time, imu[0], imu[1], imu[2],
          time, imu[3], imu[4], imu[5],
          time, imu[6], imu[7], imu[8], imu[9],
          time, bmp[0], bmp[1],
          time, bmp[2], bmp[3],
          time, adc[0], adc[1]);

  Serial.println(message);

  return;
}

void read_ST_BURN()
{
  HC12.readBytes(buffer, packet_size[State::ST_BURN] - 1);
  uint32_t time;
  float attitude[4];
  float nav[6];
  float P_chamber;

  memcpy(&time, buffer, 4);
  memcpy(attitude, buffer + 4, 16);
  memcpy(nav, buffer + 20, 24);
  memcpy(&P_chamber, buffer + 44, 4);

  char message[1000];
  sprintf(message, "[%07lu] [STAT] ST_BURN\n"
                   "[%07lu] [DATA] [Attitude] qx: %.7f, qy: %.7f, qz: %.7f, qw: %.7f\n"
                   "[%07lu] [DATA] [Nav] Pos: (%.7f, %.7f, %.7f), Vel: (%.7f, %.7f, %.7f)\n"
                   "[%07lu] [DATA] [P_chamber] Pressure: %.7f",
          time,
          time, attitude[0], attitude[1], attitude[2], attitude[3],
          time, nav[0], nav[1], nav[2], nav[3], nav[4], nav[5],
          time, P_chamber);

  Serial.println(message);

  return;
}

void read_ST_COAST()
{
  HC12.readBytes(buffer, packet_size[State::ST_COAST] - 1);
  uint32_t time;
  float attitude[4];
  float nav[6];

  memcpy(&time, buffer, 4);
  memcpy(attitude, buffer + 4, 16);
  memcpy(nav, buffer + 20, 24);

  char message[1000];
  sprintf(message, "[%07lu] [STAT] ST_COAST\n"
                   "[%07lu] [DATA] [Attitude] qx: %.7f, qy: %.7f, qz: %.7f, qw: %.7f\n"
                   "[%07lu] [DATA] [Nav] Pos: (%.7f, %.7f, %.7f), Vel: (%.7f, %.7f, %.7f)\n",
          time,
          time, attitude[0], attitude[1], attitude[2], attitude[3],
          time, nav[0], nav[1], nav[2], nav[3], nav[4], nav[5]);

  Serial.println(message);

  return;
}

void read_ST_DESCENT()
{
  HC12.readBytes(buffer, packet_size[State::ST_DESCENT] - 1);
  uint32_t time;
  float attitude[4];
  float nav[6];

  memcpy(&time, buffer, 4);
  memcpy(attitude, buffer + 4, 16);
  memcpy(nav, buffer + 20, 24);

  char message[1000];
  sprintf(message, "[%07lu] [STAT] ST_DESCENT\n"
                   "[%07lu] [DATA] [Attitude] qx: %.7f, qy: %.7f, qz: %.7f, qw: %.7f\n"
                   "[%07lu] [DATA] [Nav] Pos: (%.7f, %.7f, %.7f), Vel: (%.7f, %.7f, %.7f)\n",
          time,
          time, attitude[0], attitude[1], attitude[2], attitude[3],
          time, nav[0], nav[1], nav[2], nav[3], nav[4], nav[5]);

  Serial.println(message);

  return;
}

void read_ST_LANDED()
{
  HC12.readBytes(buffer, packet_size[State::ST_LANDED] - 1);
  uint32_t time;
  float gps[4];

  memcpy(&time, buffer, 4);
  memcpy(gps, buffer + 4, 16);

  char message[1000];
  sprintf(message, "[%07lu] [STAT] ST_LANDED\n"
                   "[%07lu] [DATA] [GPS] Lat: %.7f, Lon: %.7f, Alt: %.7f, Geo: %.7f\n",
          time,
          time, gps[0], gps[1], gps[2], gps[3]);

  Serial.println(message);

  return;
}