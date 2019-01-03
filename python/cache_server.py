"""
Resolves 20017 Hashcode problem.
See task description in the hashcode2017_qualification_task.pdf file.
"""
import os

import time


class Video(object):
    def __str__(self):
        return '{} {}'.format(self.id, self.size)

    def __init__(self, id, size):
        self.size = int(size)
        self.id = int(id)
        self.cacheable = True


class CacheServer(object):
    def __str__(self):
        return '{} {}'.format(self.id, self.capacity, self.videos)

    def __init__(self, id, capacity):
        self.id = id
        self.videos = []
        self.remaining_space = capacity
        self.used = False


class Request(object):
    def __init__(self, video_id, endpoint_id, count):
        self.video_id = video_id
        self.endpoint_id = endpoint_id
        self.count = count


class Endpoint(object):
    def __init__(self, endpoint_id, dt_latency, connections_count):
        self.id = endpoint_id
        self.dt_latency = dt_latency
        self.connections_count = connections_count
        self.cache_servers_map = {}


class VideoProcessing(object):
    def __init__(self, videos, endpoints_count, _, cache_servers_count, cache_capacity):
        self.videos = videos
        self.endpoints = [[] for _ in range(endpoints_count)]
        self.requests = []
        self.cache_servers = [CacheServer(id, cache_capacity) for id in range(cache_servers_count)]
        self.cache_capacity = cache_capacity
        CacheServer.capacity = cache_capacity

    def set_not_cacheable(self):
        for video in self.videos:
            if video.size > self.cache_capacity:
                video.cacheable = False

    def set_servers_conn(self):
        for server in self.cache_servers:
            server.open_conn = 0
            for endpoint in self.endpoints:
                if server.id in endpoint.cache_servers_map:
                    server.open_conn += 1

    def order_endpoints(self, reverse=False):
        self.endpoints.sort(key=lambda e: len(e.cache_servers_map.keys()), reverse=reverse)

    def attach_videos_endpoints_to_requests(self):
        for req in self.requests:
            req.video = self.videos[req.video_id]
            req.endpoint = self.endpoints[req.endpoint_id]
            req.served = False

    def filter_order_requests(self, reverse=False):
        out = []
        for r in self.requests:
            if self.videos[r.video_id].cacheable and self.endpoints[r.endpoint_id].cache_servers_map:
                out.append(r)
        self.requests = out
        self.requests.sort(key=lambda r: r.count * self.videos[r.video_id].size, reverse=True)

    def calculate_delta(self):
        return sum([v.size for v in self.videos if v.cacheable]) - (len([s for s in self.cache_servers if s.open_conn > 0]) - 1) * self.cache_capacity

    def endpoints_weight_map(self):
        endpoints_weight_map = {}
        for r in self.requests:
            if self.videos[r.video_id].cacheable:
                endpoints_weight_map[r.endpoint_id] = endpoints_weight_map.get(r.endpoint_id, 0) + r.count * self.videos[r.video_id].size
        return endpoints_weight_map

    def build_out(self):
        c_dir = os.path.dirname(os.path.abspath(__file__))
        self.set_not_cacheable()
        self.set_servers_conn()
        self.filter_order_requests()
        self.attach_videos_endpoints_to_requests()
        for request in self.requests:
            try:
                servers_by_latency = sorted(request.endpoint.cache_servers_map.items(), key=lambda item: item[1])
            except IndexError:
                continue
            for cache_server in servers_by_latency:
                s = self.cache_servers[cache_server[0]]
                if s.remaining_space >= request.video.size and request.video not in s.videos:
                    s.videos.append(request.video)
                    s.remaining_space -= request.video.size
                    request.served = True
                    break

        servers = [s for s in self.cache_servers if s.videos]
        out = '{}\n'.format(len(servers))
        for server in servers:
            out += '{} {}\n'.format(str(server.id), ' '.join([str(v.id) for v in server.videos]))
        with open(os.path.join(c_dir, 'result'), 'w+') as f:
            f.write(out)
        return out


def read_file(filename):
    with open(filename, 'r') as f_file:
        header_conf = [int(num) for num in f_file.readline().split()]
        video_line = f_file.readline().strip()
        videos = [Video(id, size) for id, size in enumerate(video_line.split())]
        header_conf[0] = videos
        _simulator = VideoProcessing(*header_conf)
        endpoint_id = 0
        phase = 'create_endpoint'
        for line in f_file.readlines():
            if len(line.split()) == 3:
                # processing requests
                video_id, endpoint_id, count = line.split()
                video_id, endpoint_id, count = int(video_id), int(endpoint_id), int(count)
                _simulator.requests.append(Request(video_id, endpoint_id, count))
                continue
            if phase == 'create_endpoint':
                dt_latency, connections_count = line.split()
                dt_latency, connections_count = int(dt_latency), int(connections_count)
                current_endpoint = Endpoint(endpoint_id, dt_latency, connections_count)
                phase = 'fill_endpoint'
                latency_number = connections_count
            elif phase == 'fill_endpoint' and latency_number != 0:
                cache_id, latency = line.split()
                cache_id, latency = int(cache_id), int(latency)
                current_endpoint.cache_servers_map[cache_id] = latency
                latency_number -= 1
            elif phase != 'fill_requests':
                _simulator.endpoints[endpoint_id] = current_endpoint
                endpoint_id += 1
                if _simulator.endpoints[-1]:
                    phase = 'fill_requests'

        _simulator.build_out()

        return _simulator


if __name__ == '__main__':
    start = time.time()
    result = read_file('trending_today.in')

    end = time.time()
    print (time.strftime("%H:%M:%S", time.gmtime(end - start)))
