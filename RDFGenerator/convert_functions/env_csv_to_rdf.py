import csv
from datetime import datetime
from rdflib import Graph, Namespace, RDF, Literal, URIRef
import time




# 从CSV数据创建OWL文件
def create_owl_from_csv(input_file,output_file):
    # 定义命名空间
    MR = Namespace("http://www.MetroRiskOntology.org/")
    EX = Namespace("http://example.org/sensor/")

    # 创建Graph对象
    g = Graph()

    # 绑定命名空间前缀
    g.bind("mr", MR)
    g.bind("ex", EX)
    with open(input_file, "r", encoding="GBK") as file:
        reader = csv.DictReader(file)

        # 为每个传感器数据创建对应的SSN结构
        for entry in reader:
            # 处理空格问题，将空格替换为下划线
            # feature_of_interest = entry["feature_of_interest"].replace(" ", "_")
            if entry['observes']=="Temperature":
                alarm_uri=EX["AbnormalTemperature"]
                g.add((alarm_uri, RDF.type, MR.Alarm))
                g.add((alarm_uri, RDF.type, MR.EnvironmentalWarning))
                g.add((alarm_uri, RDF.type, MR.AbnormalTemperature))
                g.add((alarm_uri, MR.id,
                       Literal("AbnormalTemperature", datatype="http://www.w3.org/2001/XMLSchema#string")))
            elif entry['observes']=="Humidity":
                alarm_uri=EX["AbnormalHumidity"]
                g.add((alarm_uri, RDF.type, MR.Alarm))
                g.add((alarm_uri, RDF.type, MR.EnvironmentalWarning))
                g.add((alarm_uri, RDF.type, MR.AbnormalHumidity))
                g.add((alarm_uri, MR.id,
                       Literal("AbnormalHumidity", datatype="http://www.w3.org/2001/XMLSchema#string")))
            elif entry['observes']=="FlameTemperature"|entry['observes']=="SmokeConcentration"|entry['observes']=="HarmfulGasComponents":
                alarm_uri = EX["FireWarning"]
                g.add((alarm_uri, RDF.type, MR.Alarm))
                g.add((alarm_uri, RDF.type, MR.EnvironmentalWarning))
                g.add((alarm_uri, RDF.type, MR.FireWarning))
                g.add((alarm_uri, MR.id,
                       Literal("FireWarning", datatype="http://www.w3.org/2001/XMLSchema#string")))
            elif entry['observes']=="NoiseDecibels":
                alarm_uri = EX["AbnormalNoise"]
                g.add((alarm_uri, RDF.type, MR.Alarm))
                g.add((alarm_uri, RDF.type, MR.EnvironmentalWarning))
                g.add((alarm_uri, RDF.type, MR.AbnormalNoise))
                g.add((alarm_uri, MR.id,
                       Literal("AbnormalNoise", datatype="http://www.w3.org/2001/XMLSchema#string")))
            elif entry['observes']=="WaterFlowVelocity"|entry['observes']=="WaterDepth":
                alarm_uri = EX["FloodWarning"]
                g.add((alarm_uri, RDF.type, MR.Alarm))
                g.add((alarm_uri, RDF.type, MR.EnvironmentalWarning))
                g.add((alarm_uri, RDF.type, MR.FloodWarning))
                g.add((alarm_uri, MR.id,
                       Literal("FloodWarning", datatype="http://www.w3.org/2001/XMLSchema#string")))
            elif entry['observes']=="PM2.5Concentration"|entry['observes']=="PM10Concentration"|entry['observes']=="CO2Concentration":
                alarm_uri = EX["AirQualityWarning"]
                g.add((alarm_uri, RDF.type, MR.Alarm))
                g.add((alarm_uri, RDF.type, MR.EnvironmentalWarning))
                g.add((alarm_uri, RDF.type, MR.AirQualityWarning))
                g.add((alarm_uri, MR.id,
                       Literal("AirQualityWarning", datatype="http://www.w3.org/2001/XMLSchema#string")))

            # 创建维护预警实例
            alarm_uri = EX["MaintenanceOverdue"]
            g.add((alarm_uri, RDF.type, MR.Alarm))
            g.add((alarm_uri, RDF.type, MR.SensorWarning))
            g.add((alarm_uri, RDF.type, MR.MaintenanceOverdue))
            g.add((alarm_uri, MR.id,
                   Literal("MaintenanceOverdue", datatype="http://www.w3.org/2001/XMLSchema#string")))

            # 创建工作状态异常预警实例
            alarm_uri = EX["NotWorking"]
            g.add((alarm_uri, RDF.type, MR.AbnormalStatus))
            g.add((alarm_uri, RDF.type, MR.NotWorking))
            g.add((alarm_uri, MR.id,
                   Literal("NotWorking", datatype="http://www.w3.org/2001/XMLSchema#string")))

            # 创建观察属性实例
            observed_property_uri = EX[entry["observes"]]
            g.add((observed_property_uri, RDF.type, MR.ObservedProperty))
            g.add((observed_property_uri, RDF.type, MR.EnvironmentalProperty))
            g.add((observed_property_uri, RDF.type, MR[entry["observes"]]))
            g.add((observed_property_uri, MR.id, Literal(entry["observes"])))

            # 传感器实例
            sensor_uri = EX[entry["sensor_id"]]
            g.add((sensor_uri, RDF.type, MR.Sensor))
            g.add((sensor_uri, RDF.type, MR.EnvironmentalSensors))
            g.add((sensor_uri, RDF.type, MR[entry["sensor_type"]]))
            g.add((sensor_uri, MR.observes, observed_property_uri))
            g.add((sensor_uri, MR.sensorStatus,
                   Literal(entry["sensor_status"], datatype="http://www.w3.org/2001/XMLSchema#string")))
            g.add((sensor_uri, MR.lastMaintenanceTime,
                   Literal(entry["last_maintenance_time"], datatype="http://www.w3.org/2001/XMLSchema#dateTime")))
            g.add((sensor_uri, MR.maintenanceCycle,
                   Literal(entry["maintenance_cycle"], datatype="http://www.w3.org/2001/XMLSchema#float")))
            g.add((sensor_uri, MR.id, Literal(entry["sensor_id"])))

            # 部署信息 (Location)
            location_uri = EX[f"Location_{entry['sensor_id']}"]
            g.add((sensor_uri, MR.locatedIn, location_uri))
            g.add((location_uri, RDF.type, MR.Location))
            g.add((location_uri, MR.id, Literal(entry["location"])))

            # 创建feature_of_interest实例
            feature_of_interest_uri = EX[entry["feature_of_interest"]]
            g.add((feature_of_interest_uri, RDF.type, MR.FeatureOfInterest))
            g.add((feature_of_interest_uri, RDF.type, MR.Area))
            g.add((feature_of_interest_uri, RDF.type, MR[entry['feature_of_interest']]))
            g.add((feature_of_interest_uri, MR.id, Literal(entry['feature_of_interest'])))
            g.add((feature_of_interest_uri, MR.hasProperty, observed_property_uri))

            # 创建观测实例
            observation_uri = EX[entry["observation_id"]]
            g.add((observation_uri, RDF.type, MR.Observation))
            g.add((observation_uri, RDF.type, MR.EnvironmentalObservation))
            g.add((observation_uri, RDF.type, MR[entry["obser_type"]]))
            g.add((observation_uri, MR.madeBySensor, sensor_uri))
            g.add((sensor_uri, MR.madeObservation, observation_uri))
            g.add((observation_uri, MR.observedProperty, observed_property_uri))
            g.add((observation_uri, MR.id, Literal(entry["observation_id"])))
            g.add((observation_uri, MR.hasFeatureOfInterest, feature_of_interest_uri))
            g.add((observation_uri, MR.resultTime,
                   Literal(entry["result_time"], datatype="http://www.w3.org/2001/XMLSchema#dateTime")))
            g.add((observation_uri, MR.hasSimpleResult,
                   Literal(entry["result_value"], datatype="http://www.w3.org/2001/XMLSchema#string")))
            g.add((observation_uri, MR.hasAlarm,
                   Literal(entry["alarm_status"], datatype="http://www.w3.org/2001/XMLSchema#boolean")))
            g.add((observation_uri, MR.valueUnit,
                   Literal(entry["result_unit"], datatype="http://www.w3.org/2001/XMLSchema#string")))

            # 计算时间差并提取月份
            try:
                # 修改时间解析格式，支持带T的ISO 8601格式
                result_time = datetime.strptime(entry["result_time"], "%Y-%m-%dT%H:%M:%S")
                last_maintenance_time = datetime.strptime(entry["last_maintenance_time"], "%Y-%m-%dT%H:%M:%S")

                # 计算时间差
                time_diff = result_time - last_maintenance_time

                # 提取月份差
                time_diff_seconds = time_diff.total_seconds()
                # 将计算出的时间差（月份）添加到Observation实例
                g.add((observation_uri, MR.timedif,
                       Literal(time_diff_seconds, datatype="http://www.w3.org/2001/XMLSchema#float")))

            except Exception as e:
                print(f"Error calculating time difference for observation {entry['observation_id']}: {e}")

    g.serialize(destination=output_file, format="xml")


