//
//  ClientProtocol.swift
//  Network
//
//  Created by Cem Ege on 8.02.2025.
//

import Foundation

public protocol ClientProtocol: Sendable {
    func fetch<T: Decodable>(request: Request) async -> Result<T, NetworkError>
}
