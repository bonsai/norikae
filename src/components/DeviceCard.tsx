import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Device {
  device: string;
  cpu_architecture: string;
  bit_width: string;
  core_count: string;
  max_clock: string;
  ram: string;
  storage_flash: string;
  gpu_graphics: string;
  wifi_bt: string;
  usb_function: string;
  gpio_pins: string;
  os: string;
  price_yen_2026: string;
  main_use: string;
}

interface DeviceCardProps {
  device: Device;
}

export const DeviceCard = ({ device }: DeviceCardProps) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{device.device}</CardTitle>
      </CardHeader>
      <CardContent>
        <ul>
          <li>CPU: {device.cpu_architecture}</li>
          <li>RAM: {device.ram}</li>
          <li>ストレージ: {device.storage_flash}</li>
          <li>主な用途: {device.main_use}</li>
        </ul>
      </CardContent>
    </Card>
  );
};