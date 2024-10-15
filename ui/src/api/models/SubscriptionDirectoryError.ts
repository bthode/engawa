/* tslint:disable */
/* eslint-disable */
/**
 * Engawa
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


/**
 * 
 * @export
 */
export const SubscriptionDirectoryError = {
    Unauthorized: 'Unauthorized',
    Timeout: 'Timeout',
    Refused: 'Refused',
    Nonexistent: 'Nonexistent'
} as const;
export type SubscriptionDirectoryError = typeof SubscriptionDirectoryError[keyof typeof SubscriptionDirectoryError];


export function instanceOfSubscriptionDirectoryError(value: any): boolean {
    for (const key in SubscriptionDirectoryError) {
        if (Object.prototype.hasOwnProperty.call(SubscriptionDirectoryError, key)) {
            if (SubscriptionDirectoryError[key as keyof typeof SubscriptionDirectoryError] === value) {
                return true;
            }
        }
    }
    return false;
}

export function SubscriptionDirectoryErrorFromJSON(json: any): SubscriptionDirectoryError {
    return SubscriptionDirectoryErrorFromJSONTyped(json, false);
}

export function SubscriptionDirectoryErrorFromJSONTyped(json: any, ignoreDiscriminator: boolean): SubscriptionDirectoryError {
    return json as SubscriptionDirectoryError;
}

export function SubscriptionDirectoryErrorToJSON(value?: SubscriptionDirectoryError | null): any {
    return value as any;
}

export function SubscriptionDirectoryErrorToJSONTyped(value: any, ignoreDiscriminator: boolean): SubscriptionDirectoryError {
    return value as SubscriptionDirectoryError;
}

